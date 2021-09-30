from typing import Dict, List, Optional, Tuple

from django.db import connection

from baserow.contrib.database import models
from baserow.contrib.database.fields.field_converters import FormulaFieldConverter
from baserow.contrib.database.fields.models import FormulaField, Field
from baserow.contrib.database.fields.registries import field_type_registry
from baserow.contrib.database.formula.registries import formula_type_handler_registry
from baserow.contrib.database.formula.types.type_handler import (
    BaserowFormulaTypeType,
)
from baserow.contrib.database.formula.types.type_types import (
    BaserowFormulaType,
)
from baserow.contrib.database.formula.types.table_typer import (
    TypedFieldWithReferences,
    TypedBaserowTable,
    type_all_fields_in_table,
)
from baserow.contrib.database.views.handler import ViewHandler


def _check_if_formula_type_change_requires_drop_recreate(
    old_formula_field: FormulaField, new_type: BaserowFormulaType
):
    old_formula_field_type = old_formula_field.formula_type
    old_handler: BaserowFormulaTypeType = formula_type_handler_registry.get(
        old_formula_field_type
    )
    old_type = old_handler.construct_type_from_formula_field(old_formula_field)
    return new_type.should_recreate_when_old_type_was(old_type)


def _recreate_field_if_required(
    table: "models.Table",
    old_field: FormulaField,
    new_type: BaserowFormulaType,
    new_formula_field: FormulaField,
):
    if _check_if_formula_type_change_requires_drop_recreate(old_field, new_type):
        model = table.get_model(fields=[new_formula_field], typed_table=False)
        FormulaFieldConverter().alter_field(
            old_field,
            new_formula_field,
            model,
            model,
            model._meta.get_field(old_field.db_column),
            model._meta.get_field(new_formula_field.db_column),
            None,
            connection,
        )


def _calculate_and_save_updated_fields(
    table: "models.Table",
    field_id_to_typed_field: Dict[int, TypedFieldWithReferences],
    field_which_changed=None,
) -> List[Field]:
    other_changed_fields = {}
    for typed_field in field_id_to_typed_field.values():
        new_field = typed_field.new_field
        if not isinstance(new_field, FormulaField):
            continue

        typed_formula_expression = typed_field.typed_expression
        formula_field_type = typed_formula_expression.expression_type
        # noinspection PyTypeChecker
        original_formula_field: FormulaField = typed_field.original_field

        field_id = original_formula_field.id
        checking_field_which_changed = (
            field_which_changed is not None and field_which_changed.id == field_id
        )
        if checking_field_which_changed:
            formula_field_type.raise_if_invalid()

        if not (new_field.same_as(original_formula_field)):
            new_field.save()
            ViewHandler().field_type_changed(new_field)
            if not checking_field_which_changed:
                other_changed_fields[new_field.id] = new_field
                _recreate_field_if_required(
                    table, original_formula_field, formula_field_type, new_field
                )

    if field_which_changed is not None:
        # All fields that depend on the field_which_changed need to have their
        # values recalculated as a result, even if their formula or type did not
        # change as a result.
        field_id_to_typed_field[field_which_changed.id].add_all_missing_valid_parents(
            other_changed_fields, field_id_to_typed_field
        )

    return list(other_changed_fields.values())


class TypedBaserowTableWithUpdatedFields(TypedBaserowTable):
    """
    A wrapper class containing all the typed fields in a type and additionally
    any fields which have been updated as a result of the typing of the table (possibly
    due to an initially_updated_field).
    """

    def __init__(
        self,
        typed_fields: Dict[int, TypedFieldWithReferences],
        table: "models.Table",
        initially_updated_field: Optional[Field],
        updated_fields: List[Field],
    ):
        super().__init__(typed_fields)
        self.table = table
        self.updated_initial_field = initially_updated_field
        self.updated_fields = updated_fields
        if self.updated_initial_field is not None:
            self.all_updated_fields = [self.updated_initial_field] + self.updated_fields
        else:
            self.all_updated_fields = self.updated_fields
        self.model = self.table.get_model(
            field_ids=[],
            fields=self.all_updated_fields,
            typed_table=self,
        )

    def update_values_for_all_updated_fields(self):
        """
        Does a single large update which refreshes the values of all fields which were
        updated in the table as a result of a field change.
        :return:
        """

        all_fields_update_dict = {}
        for updated_field in self.all_updated_fields:
            field_type = field_type_registry.get_by_model(updated_field)
            expr = field_type.expression_to_update_field_after_related_field_changes(
                updated_field, self.model
            )
            if expr is not None:
                all_fields_update_dict[f"field_{updated_field.id}"] = expr

        # Also update trash rows so when restored they immediately have correct formula
        # values.
        self.model.objects_and_trash.update(**all_fields_update_dict)


def type_table_and_update_fields(table: "models.Table"):
    """
    This will retype all formula fields in the table, update their definitions in the
    database and return a wrapper class which can then be used to trigger a
    recalculation of the changed fields at an appropriate time.

    :param table: The table from which the field was deleted.
    :return: A wrapper object containing all updated fields and all types for fields in
        the table. The updated fields have not yet had their values recalculated as a
        and it is up to you to call pdate_values_for_all_updated_fields when appropriate
        otherwise those fields might have stale data.
    """

    typed_fields = type_all_fields_in_table(table)
    updated_fields = _calculate_and_save_updated_fields(table, typed_fields)
    return TypedBaserowTableWithUpdatedFields(typed_fields, table, None, updated_fields)


def type_table_and_update_fields_given_changed_field(
    table: "models.Table", initial_field: Field
) -> Tuple["TypedBaserowTableWithUpdatedFields", Field]:
    """
    Given the provided field has been changed in some way this will retype all formula
    fields in the table, update their definitions in the database and return a wrapper
    class which can then be used to trigger a recalculation of the changed fields at
    an appropriate time.

    :param table: The table from which the field was deleted.
    :param initial_field: The field which was changed initially.
    :return: A wrapper object containing all updated fields and all types for fields in
        the table. The updated fields have not yet had their values recalculated as a
        result of the intial_field field change and it is up to you to call
        update_values_for_all_updated_fields when appropriate otherwise those fields
        will have stale data.
    """

    typed_fields = type_all_fields_in_table(table)
    updated_fields = _calculate_and_save_updated_fields(
        table, typed_fields, field_which_changed=initial_field
    )

    if isinstance(initial_field, FormulaField):
        typed_changed_field = typed_fields[initial_field.id].new_field
    else:
        typed_changed_field = initial_field

    return (
        TypedBaserowTableWithUpdatedFields(
            typed_fields, table, typed_changed_field, updated_fields
        ),
        typed_changed_field,
    )


def type_table_and_update_fields_given_deleted_field(
    table: "models.Table", deleted_field_id: int, deleted_field_name: str
):
    """
    Given a field with the provided name and id has been deleted will retype all formula
    fields in the table, update their definitions in the database and return a wrapper
    class which can then be used to trigger a recalculation of the changed fields at
    an appropriate time.

    Any formulas which reference the deleted field will be changed to have an invalid
    type. Those formulas will also have their actual formula changed replacing any
    field_by_id references to deleted_field_id with a field reference to the
    deleted_field_name.

    :param table: The table from which the field was deleted.
    :param deleted_field_id: The id of the field before it was deleted.
    :param deleted_field_name: The name of the field before it was deleted.
    :return: A wrapper object containing all updated fields and all types for fields in
        the table. The updated fields have not yet had their values recalculated as a
        result of the field deletion and it is up to you to call
        update_values_for_all_updated_fields when appropriate otherwise those fields
        will have stale data.
    """

    typed_fields = type_all_fields_in_table(
        table, {deleted_field_id: deleted_field_name}
    )
    updated_fields = _calculate_and_save_updated_fields(table, typed_fields)
    return TypedBaserowTableWithUpdatedFields(typed_fields, table, None, updated_fields)
