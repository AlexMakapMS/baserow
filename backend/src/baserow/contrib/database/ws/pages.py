from baserow.contrib.database.views.exceptions import ViewDoesNotExist
from baserow.contrib.database.views.handler import ViewHandler
from baserow.ws.registries import PageType

from baserow.core.exceptions import UserNotInGroup
from baserow.contrib.database.table.handler import TableHandler
from baserow.contrib.database.table.exceptions import TableDoesNotExist


class TablePageType(PageType):
    type = "table"
    parameters = ["table_id"]

    def can_add(self, user, web_socket_id, table_id, **kwargs):
        """
        The user should only have access to this page if the table exists and if he
        has access to the table.
        """

        if not table_id:
            return False

        try:
            handler = TableHandler()
            table = handler.get_table(table_id)
            table.database.group.has_user(user, raise_error=True)
        except (UserNotInGroup, TableDoesNotExist):
            return False

        return True

    def get_group_name(self, table_id, **kwargs):
        return f"table-{table_id}"


class PublicViewPageType(PageType):
    type = "view"
    parameters = ["slug"]

    def can_add(self, user, web_socket_id, slug, **kwargs):
        """
        The user should only have access to this page if the view exists and it is
        public or they have access to the group.
        """

        if not slug:
            return False

        try:
            handler = ViewHandler()
            handler.get_public_view_by_slug(user, slug)
        except ViewDoesNotExist:
            return False

        return True

    def get_group_name(self, slug, **kwargs):
        return f"view-{slug}"
