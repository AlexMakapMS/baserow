from django.contrib.contenttypes.models import ContentType
from django.db import models

from baserow.contrib.builder.pages.models import Page
from baserow.core.mixins import (
    CreatedAndUpdatedOnMixin,
    FractionOrderableMixin,
    HierarchicalModelMixin,
    PolymorphicContentTypeMixin,
    TrashableModelMixin,
)


class ExpressionField(models.TextField):
    """
    An expression that can reference a data source, a formula or a plain value.
    """


def get_default_element_content_type():
    return ContentType.objects.get_for_model(Element)


class Element(
    HierarchicalModelMixin,
    TrashableModelMixin,
    CreatedAndUpdatedOnMixin,
    FractionOrderableMixin,
    PolymorphicContentTypeMixin,
    models.Model,
):
    """
    This model represents a page element. An element is a piece of the page that
    display an information or something the user can interact with.
    """

    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    order = models.DecimalField(
        help_text="Lowest first.",
        max_digits=40,
        decimal_places=20,
        editable=False,
        default=1,
    )
    content_type = models.ForeignKey(
        ContentType,
        verbose_name="content type",
        related_name="page_elements",
        on_delete=models.SET(get_default_element_content_type),
    )

    class Meta:
        ordering = ("order", "id")

    def get_parent(self):
        return self.page

    @classmethod
    def get_last_order(cls, page: Page):
        """
        Returns the last order for the given page.

        :param Page: The page we want the order for.
        :return: The last order.
        """

        queryset = Element.objects.filter(page=page)
        return cls.get_highest_order_of_queryset(queryset)[0]

    @classmethod
    def get_unique_order_before_element(cls, before: "Element"):
        """
        Returns a safe order value before the given element in the given page.

        :param page: The page we want the order for.
        :param before: The element before which we want the safe order
        :raises CannotCalculateIntermediateOrder: If it's not possible to find an
            intermediate order. The full order of the items must be recalculated in this
            case before calling this method again.
        :return: The order value.
        """

        queryset = Element.objects.filter(page=before.page)
        return cls.get_unique_orders_before_item(before, queryset)[0]


class BaseTextElement(Element):
    """
    Base class for text elements.
    """

    value = ExpressionField(default="")

    class Meta:
        abstract = True


class HeadingElement(BaseTextElement):
    """
    A Heading element to display a title.
    """

    class HeadingLevel(models.IntegerChoices):
        H1 = 1
        H2 = 2
        H3 = 3
        H4 = 4
        H5 = 5

    level = models.IntegerField(
        choices=HeadingLevel.choices, default=1, help_text="The level of the heading"
    )


class ParagraphElement(BaseTextElement):
    """
    A simple paragraph.
    """
