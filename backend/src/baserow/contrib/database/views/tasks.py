from typing import Optional

from django.db import transaction

from baserow.config.celery import app


@app.task(bind=True, queue="export")
def update_view_index(
    self, view_id: int, previous_view_index_key: Optional[str] = None
):
    """
    Create the new index for the provided view if needed. If the
    previous_view_index_key is provided and it's not used by any other view
    then it will be removed.

    :param view_id: The id of the view for which the index should be
        updated.
    :param previous_view_index_key: The key of the previous index that should
    """

    from baserow.contrib.database.views.handler import ViewHandler

    with transaction.atomic():
        view_handler = ViewHandler()
        view = view_handler.get_view(view_id)
        view_handler._update_view_index(view, previous_view_index_key)
