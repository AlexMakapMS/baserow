from typing import Optional

from django.db.models import Q

from baserow.contrib.builder.elements.models import Element
from baserow.contrib.builder.object_scopes import BuilderObjectScopeType
from baserow.contrib.builder.page.object_scopes import BuilderPageObjectScopeType
from baserow.core.object_scopes import ApplicationObjectScopeType, GroupObjectScopeType
from baserow.core.registries import ObjectScopeType, object_scope_type_registry
from baserow.core.types import ContextObject


class BuilderElementObjectScopeType(ObjectScopeType):
    type = "builder_element"
    model_class = Element

    def get_parent_scope(self) -> Optional["ObjectScopeType"]:
        return object_scope_type_registry.get("builder_page")

    def get_parent(self, context: ContextObject) -> Optional[ContextObject]:
        return context.page

    def get_enhanced_queryset(self):
        return self.get_base_queryset().prefetch_related(
            "page", "page__builder", "page__builder__group"
        )

    def get_filter_for_scope_type(self, scope_type, scopes):
        if scope_type.type == GroupObjectScopeType.type:
            return Q(page__builder__group__in=[s.id for s in scopes])

        if (
            scope_type.type == BuilderObjectScopeType.type
            or scope_type.type == ApplicationObjectScopeType.type
        ):
            return Q(page__builder__in=[s.id for s in scopes])

        if scope_type.type == BuilderPageObjectScopeType.type:
            return Q(page__in=[s.id for s in scopes])

        raise TypeError("The given type is not handled.")
