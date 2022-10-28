from baserow_enterprise.role.operations import AssignRoleGroupOperationType
from baserow_enterprise.teams.operations import (
    CreateTeamOperationType,
    CreateTeamSubjectOperationType,
    DeleteTeamOperationType,
    DeleteTeamSubjectOperationType,
    ListTeamsOperationType,
    ListTeamSubjectsOperationType,
    ReadTeamOperationType,
    ReadTeamSubjectOperationType,
    RestoreTeamOperationType,
    UpdateTeamOperationType,
)
from baserow_premium.row_comments.operations import (
    CreateRowCommentsOperationType,
    ReadRowCommentsOperationType,
)

from baserow.contrib.database.airtable.operations import (
    RunAirtableImportJobOperationType,
)
from baserow.contrib.database.export.operations import ExportTableOperationType
from baserow.contrib.database.fields.operations import (
    CreateFieldOperationType,
    DeleteFieldOperationType,
    DuplicateFieldOperationType,
    ListFieldsOperationType,
    ReadAggregationDatabaseTableOperationType,
    ReadFieldOperationType,
    RestoreFieldOperationType,
    UpdateFieldOperationType,
)
from baserow.contrib.database.formula import TypeFormulaOperationType
from baserow.contrib.database.operations import (
    CreateTableDatabaseTableOperationType,
    ListTablesDatabaseTableOperationType,
    OrderTablesDatabaseTableOperationType,
)
from baserow.contrib.database.rows.operations import (
    DeleteDatabaseRowOperationType,
    MoveRowDatabaseRowOperationType,
    ReadAdjacentRowDatabaseRowOperationType,
    ReadDatabaseRowOperationType,
    RestoreDatabaseRowOperationType,
    UpdateDatabaseRowOperationType,
)
from baserow.contrib.database.table.operations import (
    CreateRowDatabaseTableOperationType,
    DeleteDatabaseTableOperationType,
    DuplicateDatabaseTableOperationType,
    ImportRowsDatabaseTableOperationType,
    ListAggregationDatabaseTableOperationType,
    ListenToAllDatabaseTableEventsOperationType,
    ListRowNamesDatabaseTableOperationType,
    ListRowsDatabaseTableOperationType,
    ReadDatabaseTableOperationType,
    RestoreDatabaseTableOperationType,
    UpdateDatabaseTableOperationType,
)
from baserow.contrib.database.tokens.operations import (
    CreateTokenOperationType,
    ReadTokenOperationType,
    UseTokenOperationType,
)
from baserow.contrib.database.views.operations import (
    CreateViewDecorationOperationType,
    CreateViewFilterOperationType,
    CreateViewOperationType,
    CreateViewSortOperationType,
    DeleteViewDecorationOperationType,
    DeleteViewFilterOperationType,
    DeleteViewOperationType,
    DeleteViewSortOperationType,
    DuplicateViewOperationType,
    ListViewDecorationOperationType,
    ListViewFilterOperationType,
    ListViewsOperationType,
    ListViewSortOperationType,
    OrderViewsOperationType,
    ReadViewDecorationOperationType,
    ReadViewFieldOptionsOperationType,
    ReadViewFilterOperationType,
    ReadViewOperationType,
    ReadViewsOrderOperationType,
    ReadViewSortOperationType,
    RestoreViewOperationType,
    UpdateViewDecorationOperationType,
    UpdateViewFieldOptionsOperationType,
    UpdateViewFilterOperationType,
    UpdateViewOperationType,
    UpdateViewSlugOperationType,
    UpdateViewSortOperationType,
)
from baserow.contrib.database.webhooks.operations import (
    CreateWebhookOperationType,
    DeleteWebhookOperationType,
    ListTableWebhooksOperationType,
    ReadWebhookOperationType,
    TestTriggerWebhookOperationType,
    UpdateWebhookOperationType,
)
from baserow.core.operations import (
    CreateApplicationsGroupOperationType,
    CreateInvitationsGroupOperationType,
    DeleteApplicationOperationType,
    DeleteGroupInvitationOperationType,
    DeleteGroupOperationType,
    DeleteGroupUserOperationType,
    DuplicateApplicationOperationType,
    ListApplicationsGroupOperationType,
    ListGroupUsersGroupOperationType,
    ListInvitationsGroupOperationType,
    OrderApplicationsOperationType,
    ReadApplicationOperationType,
    ReadGroupOperationType,
    ReadInvitationGroupOperationType,
    RestoreApplicationOperationType,
    RestoreGroupOperationType,
    UpdateApplicationOperationType,
    UpdateGroupInvitationType,
    UpdateGroupOperationType,
    UpdateGroupUserOperationType,
)
from baserow.core.snapshots.operations import (
    CreateSnapshotApplicationOperationType,
    DeleteApplicationSnapshotOperationType,
    ListSnapshotsApplicationOperationType,
    RestoreApplicationSnapshotOperationType,
)
from baserow.core.trash.operations import (
    EmptyApplicationTrashOperationType,
    EmptyGroupTrashOperationType,
    ReadApplicationTrashOperationType,
    ReadGroupTrashOperationType,
)

NO_ROLE_OPS = []
VIEWER_OPS = NO_ROLE_OPS + [
    ReadGroupOperationType,
    ListApplicationsGroupOperationType,
    ListTablesDatabaseTableOperationType,
    ReadApplicationOperationType,
    ReadDatabaseTableOperationType,
    ListRowsDatabaseTableOperationType,
    ReadDatabaseRowOperationType,
    ReadViewOperationType,
    ReadFieldOperationType,
    ListViewSortOperationType,
    ReadViewFieldOptionsOperationType,
    ReadViewDecorationOperationType,
    ListViewDecorationOperationType,
    ListViewFilterOperationType,
    ListViewsOperationType,
    ListFieldsOperationType,
    ListAggregationDatabaseTableOperationType,
    ReadAggregationDatabaseTableOperationType,
    ReadAdjacentRowDatabaseRowOperationType,
    ListRowNamesDatabaseTableOperationType,
    ReadViewFilterOperationType,
    ListenToAllDatabaseTableEventsOperationType,
    ReadViewsOrderOperationType,
    ReadViewSortOperationType,
]
COMMENTER_OPS = VIEWER_OPS + [
    CreateRowCommentsOperationType,
    ReadRowCommentsOperationType,
]
EDITOR_OPS = COMMENTER_OPS + [
    CreateRowDatabaseTableOperationType,
    UpdateDatabaseRowOperationType,
    DeleteDatabaseRowOperationType,
    ExportTableOperationType,
    MoveRowDatabaseRowOperationType,
    ImportRowsDatabaseTableOperationType,
    ListGroupUsersGroupOperationType,
    RestoreDatabaseRowOperationType,
    ListTeamsOperationType,
    ListTeamSubjectsOperationType,
    ReadTeamOperationType,
    ReadTeamSubjectOperationType,
]
BUILDER_OPS = EDITOR_OPS + [
    CreateTableDatabaseTableOperationType,
    UpdateDatabaseTableOperationType,
    DeleteDatabaseTableOperationType,
    RestoreDatabaseTableOperationType,
    DeleteDatabaseRowOperationType,
    CreateViewOperationType,
    CreateFieldOperationType,
    UpdateViewDecorationOperationType,
    TestTriggerWebhookOperationType,
    ListTableWebhooksOperationType,
    DuplicateFieldOperationType,
    CreateViewDecorationOperationType,
    DeleteFieldOperationType,
    RestoreFieldOperationType,
    UpdateFieldOperationType,
    TypeFormulaOperationType,
    RunAirtableImportJobOperationType,
    OrderTablesDatabaseTableOperationType,
    OrderApplicationsOperationType,
    UpdateViewOperationType,
    DeleteViewOperationType,
    RestoreViewOperationType,
    DuplicateViewOperationType,
    UpdateWebhookOperationType,
    CreateViewFilterOperationType,
    UpdateViewFilterOperationType,
    DeleteViewFilterOperationType,
    DeleteViewDecorationOperationType,
    CreateWebhookOperationType,
    DeleteWebhookOperationType,
    ReadWebhookOperationType,
    OrderViewsOperationType,
    UpdateViewFieldOptionsOperationType,
    CreateApplicationsGroupOperationType,
    DeleteViewSortOperationType,
    UpdateViewSlugOperationType,
    RestoreApplicationSnapshotOperationType,
    ListSnapshotsApplicationOperationType,
    DeleteApplicationSnapshotOperationType,
    CreateSnapshotApplicationOperationType,
    DeleteApplicationOperationType,
    RestoreApplicationOperationType,
    ReadApplicationTrashOperationType,
    DuplicateApplicationOperationType,
    UpdateApplicationOperationType,
    UpdateViewSortOperationType,
    DuplicateDatabaseTableOperationType,
    CreateViewSortOperationType,
    ReadGroupTrashOperationType,
    CreateTokenOperationType,
    ReadTokenOperationType,
    UseTokenOperationType,
]
ADMIN_OPS = BUILDER_OPS + [
    UpdateGroupOperationType,
    DeleteGroupOperationType,
    DeleteDatabaseRowOperationType,
    ReadInvitationGroupOperationType,
    AssignRoleGroupOperationType,
    DeleteGroupUserOperationType,
    DeleteGroupInvitationOperationType,
    UpdateGroupUserOperationType,
    CreateInvitationsGroupOperationType,
    ListInvitationsGroupOperationType,
    UpdateGroupInvitationType,
    CreateTeamOperationType,
    UpdateTeamOperationType,
    DeleteTeamOperationType,
    CreateTeamSubjectOperationType,
    DeleteTeamSubjectOperationType,
    RestoreTeamOperationType,
    RestoreGroupOperationType,
    EmptyApplicationTrashOperationType,
    EmptyGroupTrashOperationType,
]
default_roles = {
    "ADMIN": ADMIN_OPS,
    "BUILDER": BUILDER_OPS,
    "EDITOR": EDITOR_OPS,
    "COMMENTER": COMMENTER_OPS,
    "VIEWER": VIEWER_OPS,
    "NO_ROLE": NO_ROLE_OPS,
}
