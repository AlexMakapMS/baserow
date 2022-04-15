import pytest

from baserow.core.actions.scopes import (
    RootActionScopeType,
)
from baserow.core.actions.handler import ActionHandler
from baserow.core.actions.registries import (
    action_type_registry,
)
from baserow.core.actions.group_actions import (
    CreateGroupActionType,
    UpdateGroupActionType,
)
from baserow.core.models import Group
from baserow.core.utils import mark_as_locked


@pytest.mark.django_db
def test_can_undo_creating_group(data_fixture, django_assert_num_queries):
    session_id = "session-id"
    user = data_fixture.create_user(session_id=session_id)

    group_user = action_type_registry.get_by_type(CreateGroupActionType).do(
        user, "test"
    )
    group = group_user.group

    ActionHandler.undo(user, [RootActionScopeType.value()], session_id)

    assert Group.objects.filter(pk=group.id).count() == 0


@pytest.mark.django_db
def test_can_undo_redo_creating_group(data_fixture, django_assert_num_queries):
    session_id = "session-id"
    user = data_fixture.create_user(session_id=session_id)

    group_user = action_type_registry.get_by_type(CreateGroupActionType).do(
        user, "test"
    )
    group2_user = action_type_registry.get_by_type(CreateGroupActionType).do(
        user, "test2"
    )
    group = group_user.group
    group2 = group2_user.group

    ActionHandler.undo(user, [RootActionScopeType.value()], session_id)

    assert not Group.objects.filter(pk=group2.id).exists()
    assert Group.objects.filter(pk=group.id).exists()

    ActionHandler.redo(user, [RootActionScopeType.value()], session_id)

    assert Group.objects.filter(pk=group2.id).exists()
    assert Group.objects.filter(pk=group.id).exists()


@pytest.mark.django_db
def test_can_undo_updating_group(data_fixture, django_assert_num_queries):
    session_id = "session-id"
    user = data_fixture.create_user(session_id=session_id)

    group_user = action_type_registry.get_by_type(CreateGroupActionType).do(
        user, "test"
    )

    updated_group = action_type_registry.get_by_type(UpdateGroupActionType).do(
        user, mark_as_locked(group_user.group), "new name"
    )

    assert updated_group.name == "new name"
    ActionHandler.undo(user, [RootActionScopeType.value()], session_id)
    updated_group.refresh_from_db()
    assert updated_group.name == "test"
