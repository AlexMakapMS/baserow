from cachalot import utils as cachalot_utils


def patch_cachalot_for_baserow(baserow_table_name_prefix="database_table_"):
    """
    This function patches the cachalot library to make it work with baserow
    dynamic models. The problem is that the only way to limit what cachalot
    caches is to provide a list of tables, but baserow creates dynamic models
    on the fly, so we can't know what tables will be created in advance. This
    function patches the cachalot library to make it work with baserow dynamic
    models.

    `filter_cachable` and `is_cachable` are called to invalidate the cache when
    a table is changed.
    `are_all_cachable` is called to check if a query can be
    cached.
    """

    original_filter_cachable = cachalot_utils.filter_cachable

    def patched_filter_cachable(tables):
        return original_filter_cachable(tables).union(
            set(filter(lambda t: t.startswith(baserow_table_name_prefix), tables))
        )

    cachalot_utils.filter_cachable = patched_filter_cachable

    original_is_cachable = cachalot_utils.is_cachable

    def patched_is_cachable(table):
        is_baserow_table = table.startswith(baserow_table_name_prefix)
        return is_baserow_table or original_is_cachable(table)

    cachalot_utils.is_cachable = patched_is_cachable

    original_are_all_cachable = cachalot_utils.are_all_cachable

    def patched_are_all_cachable(tables):
        """
        This patch works because cachalot does not explicitly set this thread
        local variable, but it assumes to be True by default if CACHALOT_ENABLED
        is not set otherwise. Since we are explicitly setting it to True in our
        code for the query we want to cache, we can check if the value it's True
        to remove our dynamic tables from the list of tables that cachalot will
        check.
        """

        from cachalot.api import LOCAL_STORAGE

        cachalot_enabled = getattr(LOCAL_STORAGE, "cachalot_enabled", False)
        if cachalot_enabled:
            tables = set(
                t for t in tables if not t.startswith(baserow_table_name_prefix)
            )
        return original_are_all_cachable(tables)

    cachalot_utils.are_all_cachable = patched_are_all_cachable
