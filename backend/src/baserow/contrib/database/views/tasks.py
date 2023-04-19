from baserow.config.celery import app


@app.task(bind=True, queue="export")
def update_view_index(self, view_id: int):
    """
    Recrate the index of the provided view.
    """

    from baserow.contrib.database.views.handler import ViewHandler

    view_handler = ViewHandler()
    view = view_handler.get_view(view_id)
    view_handler._update_view_index(view)
