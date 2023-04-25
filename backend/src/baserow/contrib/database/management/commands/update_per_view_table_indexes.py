import sys

from django.core.management.base import BaseCommand

from tqdm import tqdm

from baserow.contrib.database.models import Database
from baserow.contrib.database.table.models import Table
from baserow.core.models import Workspace


class Command(BaseCommand):
    help = "Update per view table indexes."

    def add_arguments(self, parser):
        parser.add_argument(
            "--table_id",
            nargs="?",
            type=int,
            help=(
                "The table in which the indexes will be updated. "
                "If the value is None, the workspace_id or the table_id argument is required."
            ),
            default=None,
        )
        parser.add_argument(
            "--database_id",
            nargs="?",
            type=int,
            help=(
                "The database in which all the tables indexes will be updated. "
                "If the value is None, the workspace_id or the table_id argument is required."
            ),
            default=None,
        )
        parser.add_argument(
            "--workspace_id",
            nargs="?",
            type=int,
            help=(
                "The workspace in which all the tables indexes of all the databases will be updated. "
                "If the value is None, the database_id or the table_id argument is required."
            ),
            default=None,
        )

    def handle(self, *args, **options):
        workspace_id = options["workspace_id"]
        database_id = options["database_id"]
        table_id = options["table_id"]

        if workspace_id is None and database_id is None and table_id is None:
            self.stdout.write(
                self.style.ERROR(
                    "A table_id or a database_id or a workspace_id is required."
                )
            )
            sys.exit(1)

        if table_id:
            try:
                tables = [Table.objects.get(pk=table_id)]
            except Table.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f"The table with id {table_id} was not found.")
                )
                sys.exit(1)
        elif database_id:
            try:
                tables = Table.objects.filter(
                    database=Database.objects.get(pk=database_id)
                )
            except Database.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f"The database with id {database_id} was not found.")
                )
                sys.exit(1)
        elif workspace_id:
            try:
                tables = Table.objects.filter(
                    database__workspace=Workspace.objects.get(pk=workspace_id)
                )
            except Workspace.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f"The workspace with id {workspace_id} was not found.")
                )
                sys.exit(1)

        for table in tqdm(tables, desc="Updating per view indexes", unit="table"):
            print(f"Start creating/deleting per view indexes for table {table.id}")
            indexes, added, removed = table.update_per_view_indexes()
            print(
                f"{len(added)} indexes added, {len(removed)} indexes removed, {len(indexes)} indexes total for table {table.id}"
            )

        self.stdout.write(
            self.style.SUCCESS(f"Successfully updated {len(tables)} tables.")
        )
