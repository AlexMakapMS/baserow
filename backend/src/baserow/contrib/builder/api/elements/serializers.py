from django.utils.functional import lazy

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from baserow.contrib.builder.elements.models import Element
from baserow.contrib.builder.elements.registries import element_type_registry

EXPRESSION_TYPES = [
    ("plain", "Plain"),
    ("formula", "Formula"),
    ("data", "Data"),
]


class ExpressionSerializer(serializers.Serializer):
    """
    A serializer for Expressions.
    """

    type = serializers.ChoiceField(
        help_text="The type of the expression.",
        choices=EXPRESSION_TYPES,
        default="plain",
    )
    expression = serializers.CharField(
        help_text="The value of the expression.",
        allow_blank=True,
        required=False,
        default="",
    )


@extend_schema_field(ExpressionSerializer)
class ExpressionField(serializers.JSONField):
    """
    The expression field can be used to ensure the given data is an expression.
    """

    def __init__(self, *args, **kwargs):
        kwargs["default"] = kwargs.get(
            "default", lambda: {"type": "plain", "expression": ""}
        )
        super().__init__(*args, **kwargs)

    def to_internal_value(self, data):
        serializer = ExpressionSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data


class ElementSerializer(serializers.ModelSerializer):
    """
    Basic element serializer mostly for returned values.
    """

    type = serializers.SerializerMethodField(help_text="The type of the element.")

    @extend_schema_field(OpenApiTypes.STR)
    def get_type(self, instance):
        return element_type_registry.get_by_model(instance.specific_class).type

    class Meta:
        model = Element
        fields = ("id", "page_id", "type", "order")
        extra_kwargs = {
            "id": {"read_only": True},
            "page_id": {"read_only": True},
            "type": {"read_only": True},
            "order": {"read_only": True, "help_text": "Lowest first."},
        }


class CreateElementSerializer(serializers.ModelSerializer):
    """
    This serializer allow to set the type of an element and the element id before which
    we want to insert the new element.
    """

    type = serializers.ChoiceField(
        choices=lazy(element_type_registry.get_types, list)(),
        required=True,
        help_text="The type of the element.",
    )
    before_id = serializers.IntegerField(
        required=False,
        help_text="If provided, creates the element before the element with the "
        "given id.",
    )

    class Meta:
        model = Element
        fields = ("before_id", "type")


class UpdateElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Element
        fields = []


class OrderElementsSerializer(serializers.Serializer):
    element_ids = serializers.ListField(
        child=serializers.IntegerField(),
        help_text="The ids of the elements in the order they are supposed to be set in",
    )
