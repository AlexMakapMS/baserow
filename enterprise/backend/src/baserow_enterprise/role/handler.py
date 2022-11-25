from functools import cmp_to_key
from typing import Any, Dict, List, Optional, Tuple, Union

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.models import ContentType

from baserow.core.handler import CoreHandler
from baserow.core.models import Group, GroupUser
from baserow.core.registries import (
    object_scope_type_registry,
    permission_manager_type_registry,
    subject_type_registry,
)
from baserow_enterprise.exceptions import ScopeNotExist, SubjectNotExist
from baserow_enterprise.models import RoleAssignment
from baserow_enterprise.role.models import Role
from baserow_enterprise.teams.models import Team

User = get_user_model()


def compare_scopes(a, b):
    a_scope_type = object_scope_type_registry.get_by_model(a[0])
    b_scope_type = object_scope_type_registry.get_by_model(b[0])
    a_includes_b = object_scope_type_registry.scope_type_includes_scope_type(
        a_scope_type, b_scope_type
    )
    b_includes_a = object_scope_type_registry.scope_type_includes_scope_type(
        b_scope_type, a_scope_type
    )

    if a_includes_b and b_includes_a:
        return 0
    if a_includes_b:
        return -1
    if b_includes_a:
        return 1


class RoleAssignmentHandler:
    FALLBACK_ROLE = "NO_ACCESS"
    ADMIN_ROLE = "ADMIN"
    NO_ACCESS_ROLE = "NO_ACCESS"

    @classmethod
    def _get_role_caches(cls):
        if not getattr(cls, "_init", False):
            cls._init = True
            cls._role_cache_by_uid = {}
            cls._role_cache_by_id = {}
            for role in Role.objects.prefetch_related("operations").all():
                cls._role_cache_by_uid[role.uid] = role
                cls._role_cache_by_id[role.id] = role

        return cls._role_cache_by_uid, cls._role_cache_by_id

    def get_role_by_uid(self, role_uid: str, use_fallback=False) -> Role:
        """
        Returns the role for the given uid.
        If `role_uid` isn't found, we fall back to `role_fallback`.

        :param role_uid: The uid we want the role for.
        :param use_fallback: If true and the role_uid is not found, we fallback to
           the NO_ACCESS role.
        :return: A role.
        """

        # Translate MEMBER to builder for compatibility with basic "role" name.
        if role_uid == "MEMBER":
            role_uid = "BUILDER"

        try:
            if role_uid not in self._get_role_caches()[0]:
                raise Role.DoesNotExist()

            return self._get_role_caches()[0][role_uid]
        except Role.DoesNotExist:
            if use_fallback:
                return self.get_role_by_uid(self.FALLBACK_ROLE)
            else:
                raise

    def get_role_by_id(self, role_id: int) -> Role:
        """
        Returns the role for the given id.

        :param role_id: The id we want the role for.
        :return: A role.
        """

        if role_id not in self._get_role_caches()[1]:
            raise Role.DoesNotExist()

        return self._get_role_caches()[1][role_id]

    def get_current_role_assignment(
        self,
        subject: Union[AbstractUser, Team],
        group: Group,
        scope: Optional[Any] = None,
    ) -> Union[RoleAssignment, None]:
        """
        Returns the current assigned role for the given Group/Subject/Scope.

        :param subject: The subject we want the role for.
        :param group: The group in which you want the user or team role.
        :param scope: An optional scope on which the role applies.
        :return: The current `RoleAssignment` or `None` if no role is defined for the
            given parameters.
        """

        if scope is None:
            scope = group

        content_types = ContentType.objects.get_for_models(scope, subject)

        # If we are assigning a role to a group, we store the role uid in
        # the `.permissions` property of the `GroupUser` object instead to stay
        # compatible with other permission manager. This make it easy to switch from
        # one permission manager to another without losing nor duplicating information
        if (
            isinstance(scope, Group)
            and scope.id == group.id
            and isinstance(subject, User)
        ):
            try:
                group_user = group.get_group_user(subject)
                role = self.get_role_by_uid(group_user.permissions, use_fallback=True)
                # We need to fake a RoleAssignment instance here to keep the same
                # return interface
                return RoleAssignment(
                    subject=subject,
                    subject_id=subject.id,
                    subject_type=content_types[subject],
                    role=role,
                    group=group,
                    scope=scope,
                    scope_type=content_types[scope],
                )
            except GroupUser.DoesNotExist:
                return None

        try:
            role_assignment = RoleAssignment.objects.select_related("role").get(
                scope_id=scope.id,
                scope_type=content_types[scope],
                group=group,
                subject_id=subject.id,
                subject_type=content_types[subject],
            )

            return role_assignment
        except RoleAssignment.DoesNotExist:
            return None

    def get_sorted_subject_scope_roles(
        self, group: Group, actor: AbstractUser
    ) -> List[Tuple[Any, Role]]:
        """
        Returns the RoleAssignments for the given actor in the given group. The roles
        are ordered by position of the role scope in the object hierarchy: the highest
        parent is before the lowest.

        :param group: The group the RoleAssignments belong to.
        :param actor: The actor for whom we want the RoleAssignments for.
        :param operation: An optional Operation to select only roles containing this
            operation.
        :return: A list of tuple containing the scope and the role ordered by scope.
            The higher a scope is high in the object hierarchy, the higher the tuple in
            the list.
        """

        role_assignment_handler = RoleAssignmentHandler()

        roles = RoleAssignment.objects.filter(
            group=group,
            subject_type=ContentType.objects.get_for_model(User),
            subject_id=actor.id,
        ).exclude(scope_type=ContentType.objects.get_for_model(Group))

        # TODO potentially n-queries here with r.scope
        available_operations_per_scope = [
            (r.scope, role_assignment_handler.get_role_by_id(r.role_id)) for r in roles
        ]

        # Get the group level role by reading the GroupUser permissions property
        group_level_role = role_assignment_handler.get_role_by_uid(
            group.get_group_user(actor).permissions, use_fallback=True
        )

        available_operations_per_scope = [
            (
                group,
                group_level_role,
            )
        ] + available_operations_per_scope

        # Roles are ordered by scope size. The higher in the hierarchy, the higher
        # in the list.
        available_operations_per_scope.sort(key=cmp_to_key(compare_scopes))

        return available_operations_per_scope

    def get_computed_role(self, group, actor, context):
        role_assignments = self.get_sorted_subject_scope_roles(group, actor)
        most_precise_role = RoleAssignmentHandler().get_role_by_uid(self.NO_ACCESS_ROLE)

        for (scope, role) in role_assignments:
            if object_scope_type_registry.scope_includes_context(scope, context):
                # If any role of a scope parent of the context is ADMIN then the
                # operation is allowed even if a child creates exception.
                if role.uid == self.ADMIN_ROLE:
                    return role
                # Check if this scope includes the context. As the role assignments
                # are Sorted, the new scope is more precise than the previous one.
                # So we keep this new role.
                most_precise_role = role
            elif (
                object_scope_type_registry.scope_includes_context(context, scope)
                and role.uid != self.NO_ACCESS_ROLE
            ):
                # Here the user has a permission on a scope that is a child of the
                # context, then we grant the user permission on all read operations
                # for all parents of that scope and hence this context should be
                # readable.
                # For example, if you have a "BUILDER" role on only a table scope,
                # and the context here is the parent database of this table the
                # user should be able to read this database object so they can
                # actually have access to lower down.
                if most_precise_role.uid == self.NO_ACCESS_ROLE:
                    most_precise_role = RoleAssignmentHandler().get_role_by_uid(
                        "VIEWER"
                    )

        return most_precise_role

    def assign_role(
        self,
        subject,
        group,
        role=None,
        scope=None,
    ) -> Optional[RoleAssignment]:
        """
        Assign a role to a subject in the context of the given group over a specified
        scope.

        :param subject: The subject targeted by the role.
        :param group: The group in which we want to assign the role.
        :param role: The role we want to assign. If the role is `None` then we remove
            the current role of the subject in the group for the given scope.
        :param scope: An optional scope on which the role applies. If no scope is given
            the group is used as scope.
        :return: The created RoleAssignment if role is not `None` else `None`.
        """

        if role is None:
            # Early return, we are removing the current role.
            self.remove_role(subject, group, scope=scope)
            return

        if scope is None:
            scope = group

        subject_type = subject_type_registry.get_by_model(subject)
        if not subject_type.is_in_group(subject.id, group):
            raise SubjectNotExist()

        if not object_scope_type_registry.scope_includes_context(group, scope):
            raise ScopeNotExist()

        content_types = ContentType.objects.get_for_models(scope, subject)

        # Group level permissions are not stored as RoleAssignment records
        if scope == group and scope.id == group.id and isinstance(subject, User):
            group_user = group.get_group_user(subject)
            new_permissions = "MEMBER" if role.uid == "BUILDER" else role.uid
            CoreHandler().force_update_group_user(
                None, group_user, permissions=new_permissions
            )

            # We need to fake a RoleAssignment instance here to keep the same
            # return interface
            return RoleAssignment(
                subject=subject,
                subject_id=subject.id,
                subject_type=content_types[subject],
                role=role,
                group=group,
                scope=scope,
                scope_type=content_types[scope],
            )

        role_assignment, _ = RoleAssignment.objects.update_or_create(
            subject_id=subject.id,
            subject_type=content_types[subject],
            group=group,
            scope_id=scope.id,
            scope_type=content_types[scope],
            defaults={"role": role},
        )

        return role_assignment

    def remove_role(self, subject: Union[AbstractUser, Team], group: Group, scope=None):
        """
        Remove the role of a subject in the context of the given group over a specified
        scope.

        :param subject: The subject for whom we want to remove the role for.
        :param group: The group in which we want to remove the role.
        :param scope: An optional scope on which the existing role applied.
            If no scope is given the group is used as scope.
        """

        if scope is None:
            scope = group

        if scope == group and scope.id == group.id and isinstance(subject, User):
            group_user = group.get_group_user(subject)
            new_permissions = self.NO_ACCESS_ROLE
            CoreHandler().force_update_group_user(
                None, group_user, permissions=new_permissions
            )
            return

        content_types = ContentType.objects.get_for_models(scope, subject)

        RoleAssignment.objects.filter(
            subject_id=subject.id,
            subject_type=content_types[subject],
            group=group,
            scope_id=scope.id,
            scope_type=content_types[scope],
        ).delete()

    def get_subject(self, subject_id: int, subject_type: str):
        """
        Helper method that returns the actual subject object given the subject_id and
        the subject type.

        :param subject_id: The subject id.
        :param subject_type: The subject type.
        """

        content_type = subject_type_registry.get(subject_type).get_content_type()
        return content_type.get_object_for_this_type(id=subject_id)

    def get_scope(self, scope_id: int, scope_type: str):
        """
        Helper method that returns the actual scope object given the scope ID and
        the scope type.

        :param scope_id: The scope id.
        :param scope_type: The scope type. This type must be registered in the
            `object_scope_registry`.
        """

        scope_type = object_scope_type_registry.get(scope_type)
        content_type = ContentType.objects.get_for_model(scope_type.model_class)
        return content_type.get_object_for_this_type(id=scope_id)

    def assign_role_batch(
        self, user: AbstractUser, group: Group, values: List[Dict[str, any]]
    ):
        """
        Creates role assignments in batch, this should be used if many role assignments
        are created at once, to be more efficient.

        :return:
        """

        from baserow_enterprise.role.permission_manager import RolePermissionManagerType

        role_assignments = []
        role_assignments_to_create = []
        group_users_to_update_values = []

        no_access_role = self.get_role_by_uid(self.NO_ACCESS_ROLE)

        role_permission_manager = permission_manager_type_registry.get_by_type(
            RolePermissionManagerType
        )

        for value in values:
            if value["scope"] is None:
                value["scope"] = group

            scope_type = object_scope_type_registry.get_by_model(value["scope"])
            subject_type = subject_type_registry.get_by_model(value["subject"])

            if not subject_type.is_in_group(value["subject_id"], group):
                raise SubjectNotExist()

            if not object_scope_type_registry.scope_includes_context(
                group, value["scope"]
            ):
                raise ScopeNotExist()

            # TODO performance bottleneck
            CoreHandler().check_permissions(
                user,
                role_permission_manager.role_assignable_object_map[scope_type.type][
                    "READ"
                ].type,
                group=group,
                context=value["scope"],
            )

            role_assignment = RoleAssignment(
                subject=value["subject"],
                subject_id=value["subject_id"],
                subject_type=value["subject_type"],
                role=value["role"],
                scope=value["scope"],
                scope_id=value["scope_id"],
                scope_type=value["scope_type"],
                group=group,
            )

            if value["scope"] == group:  # Group level permissions
                if value["role"] is None:
                    value["role"] = no_access_role
                group_users_to_update_values.append(value)
            else:  # Not a group level assignment
                if value["role"] is None:  # Delete role assignment
                    self.remove_role(value["subject"], group, scope=value["scope"])
                else:  # Create or update role assignments
                    role_assignment_found = RoleAssignment.objects.filter(
                        subject_id=value["subject_id"],
                        subject_type=value["subject_type"],
                        scope_id=value["scope_id"],
                        scope_type=value["scope_type"],
                        group=group,
                    ).first()

                    if role_assignment_found:
                        role_assignment_found.role = value["role"]
                        role_assignment_found.save()
                    else:
                        role_assignments_to_create.append(role_assignment)

                    role_assignments.append(role_assignment)

        group_users_to_update_instances = GroupUser.objects.filter(
            group=group,
            user__in=[value["subject"] for value in group_users_to_update_values],
        )

        group_users_to_update_instances_map = {
            getattr(group_user.user, "id"): group_user
            for group_user in group_users_to_update_instances
        }

        for value in group_users_to_update_values:
            group_users_to_update_instances_map[
                value["subject_id"]
            ].permissions = value["role"].uid

        GroupUser.objects.bulk_update(
            group_users_to_update_instances_map.values(), ["permissions"]
        )
        RoleAssignment.objects.bulk_create(role_assignments_to_create)

        return role_assignments

    def get_role_assignments(self, group: Group, scope=None):
        """
        Helper method that returns all role assignments given a scope and group.

        :param group: The group that the scope belongs to
        :param scope: The scope used for filtering role assignments
        """

        if isinstance(scope, Group) and scope.id == group.id:
            group_users = GroupUser.objects.filter(group=group)

            role_assignments = []

            for group_user in group_users:
                role_uid = group_user.permissions
                role = self.get_role_by_uid(role_uid, use_fallback=True)
                subject = group_user.user

                # TODO we probably shouldn't do this in a loop (performance)
                content_types = ContentType.objects.get_for_models(scope, subject)
                # We need to fake a RoleAssignment instance here to keep the same
                # return interface
                role_assignments.append(
                    RoleAssignment(
                        subject=subject,
                        subject_id=subject.id,
                        subject_type=content_types[subject],
                        role=role,
                        group=group,
                        scope=scope,
                        scope_type=content_types[scope],
                    )
                )
            return role_assignments
        else:
            role_assignments = RoleAssignment.objects.filter(
                group=group,
                scope_id=scope.id,
                scope_type=ContentType.objects.get_for_model(scope),
            )
            return list(role_assignments)
