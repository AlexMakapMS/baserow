from abc import ABC

from baserow.contrib.builder.operations import BuilderOperationType


class BuilderPageOperationType(BuilderOperationType, ABC):
    context_scope_name = "builder_page"


class CreatePageOperationType(BuilderOperationType):
    type = "builder.page.create"


class DeletePageOperationType(BuilderPageOperationType):
    type = "builder.page.delete"


class ReadPageOperationType(BuilderPageOperationType):
    type = "builder.page.read"
