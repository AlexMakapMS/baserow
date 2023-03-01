from typing import Any, Dict, List

from django.db.models import QuerySet

from baserow.contrib.builder.elements.exceptions import ElementDoesNotExist
from baserow.contrib.builder.elements.models import Element
from baserow.contrib.builder.elements.registries import (
    ElementType,
    element_type_registry,
)
from baserow.contrib.builder.pages.models import Page
from baserow.core.db import specific_iterator
from baserow.core.utils import extract_allowed


class ElementHandler:
    def get_element(self, element_id: int) -> Element:
        """
        Returns an element instance from the database.

        :param element_id: The ID of the element.
        :raises ElementDoesNotExist: If the element can't be found.
        :return: The element instance.
        """

        try:
            element = (
                Element.objects.select_related(
                    "page", "page__builder", "page__builder__group"
                )
                .get(id=element_id)
                .specific
            )
        except Element.DoesNotExist:
            raise ElementDoesNotExist()

        return element

    def get_elements(
        self, page: Page, base_queryset: QuerySet = None, specific: bool = True
    ) -> List[Element]:
        """
        Gets all the specific elements of a given page.

        :param page: The page that holds the elements.
        :param base_queryset: The base queryset to use to build the query.
        :param specific: Wether or not return the generic elements or the specific
            instances.
        :return: The elements of that page.
        """

        queryset = base_queryset if base_queryset is not None else Element.objects.all()
        queryset = queryset.filter(page=page)

        if specific:
            queryset = queryset.select_related("content_type")
            return specific_iterator(queryset)
        else:
            return queryset

    def create_element(
        self, element_type: ElementType, page: Page, **kwargs
    ) -> Element:
        """
        Creates a new element for a page.

        :param element_type: The type of the element.
        :param page: The page the element exists in.
        :param kwargs: Additional attributes of the element.
        :return: The created element.
        """

        model_class = element_type.model_class

        last_order = model_class.get_last_order(page)
        element = model_class(page=page, order=last_order, **kwargs)
        element.save()

        return element

    def delete_element(self, element: Element):
        """
        Deletes an element.

        :param element: The to-be-deleted element.
        """

        element.delete()

    def update_element(self, element: Element, values: Dict[str, Any]) -> Element:
        """
        Updates and element with values. Will also check if the values are allowed
        to be set on the element first.

        :param element: The element that should be updated.
        :param values: The values that should be set on the element.
        :return: The updated element.
        """

        shared_allowed_fields = []

        element_type = element_type_registry.get_by_model(element)

        allowed_updates = extract_allowed(
            values, shared_allowed_fields + element_type.allowed_fields
        )

        for key, value in allowed_updates.items():
            setattr(element, key, value)

        element.save()

        return element

    def order_elements(self, page: Page, new_order: List[int]) -> List[int]:
        """
        Changes the order of the elements of a page.

        :param page: The page the elements exist on.
        :param new_order: The new order which they should have.
        :return: The full order of all elements after they have been ordered.
        """

        all_elements = Element.objects.filter(page=page)

        full_order = Element.order_objects(all_elements, new_order)

        return full_order
