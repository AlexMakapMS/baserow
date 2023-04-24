from django.db import transaction

from baserow.config.celery import app


@app.task(bind=True, queue="export")
def update_per_view_indexes(self, table_id: int):
    """
    Create the new index for the provided view if needed. If the
    previous_view_index_key is provided and it's not used by any other view
    then it will be removed.

    :param table_id: The id of the table for which the indexes should be
        updated.
    """

    from baserow.contrib.database.table.handler import TableHandler

    with transaction.atomic():
        table = TableHandler().get_table(table_id=table_id)
        table.update_per_view_indexes()
