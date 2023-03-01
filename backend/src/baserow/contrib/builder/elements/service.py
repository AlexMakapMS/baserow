from typing import Any, Dict, List, Optional

from django.contrib.auth.models import AbstractUser

from baserow.contrib.builder.elements.exceptions import ElementNotInPage
from baserow.contrib.builder.elements.handler import ElementHandler
from baserow.contrib.builder.elements.models import Element
from baserow.contrib.builder.elements.operations import (
    CreateElementOperationType,
    DeleteElementOperationType,
    ListElementsPageOperationType,
    OrderElementsPageOperationType,
    ReadElementOperationType,
    UpdateElementOperationType,
)
from baserow.contrib.builder.elements.registries import ElementType
from baserow.contrib.builder.elements.signals import (
    element_created,
    element_deleted,
    element_updated,
    elements_reordered,
)
from baserow.contrib.builder.pages.models import Page
from baserow.core.handler import CoreHandler


class ElementService:
    def __init__(self):
        self.handler = ElementHandler()

    def get_element(self, user: AbstractUser, element_id: int) -> Element:
        """
        Returns an element instance from the database. Also checks the user permissions.

        :param user: The user trying to get the element
        :param element_id: The ID of the element
        :return: The element instance
        """

        element = self.handler.get_element(element_id)

        CoreHandler().check_permissions(
            user,
            ReadElementOperationType.type,
            group=element.page.builder.group,
            context=element,
        )

        return element

    def get_elements(self, user: AbstractUser, page: Page) -> List[Element]:
        """
        Gets all the elements of a given page visible to the given user.

        :param user: The user trying to get the elements.
        :param page: The page that holds the elements.
        :return: The elements of that page.
        """

        CoreHandler().check_permissions(
            user,
            ListElementsPageOperationType.type,
            group=page.builder.group,
            context=page,
        )

        user_elements = CoreHandler().filter_queryset(
            user,
            ListElementsPageOperationType.type,
            Element.objects.all(),
            group=page.builder.group,
            context=page,
        )

        return self.handler.get_elements(page, base_queryset=user_elements)

    def create_element(
        self,
        user: AbstractUser,
        element_type: ElementType,
        page: Page,
        before_id: Optional[int] = None,
        **kwargs,
    ) -> Element:
        """
        Creates a new element for a page given the user permissions.

        :param user: The user trying to create the element.
        :param element_type: The type of the element.
        :param page: The page the element exists in.
        :param before_id: If set, the new element is inserted before the element with
            this id.
        :param kwargs: Additional attributes of the element.
        :return: The created element.
        """

        CoreHandler().check_permissions(
            user,
            CreateElementOperationType.type,
            group=page.builder.group,
            context=page,
        )

        new_element = self.handler.create_element(element_type, page, **kwargs)

        if before_id:
            old_order = self.handler.get_elements(page, specific=False).values_list(
                "id", flat=True
            )
            # Compute new order by inserting the element before the before_id
            new_order = []
            for element_id in old_order:
                if element_id == new_element.id:
                    continue
                if element_id == before_id:
                    new_order.append(new_element.id)
                new_order.append(element_id)

            self.handler.order_elements(page, new_order)

            # Update the order field
            new_element.refresh_from_db()

        element_created.send(self, element=new_element, before_id=before_id, user=user)

        return new_element

    def update_element(
        self, user: AbstractUser, element: Element, values: Dict[str, Any]
    ) -> Element:
        """
        Updates and element with values. Will also check if the values are allowed
        to be set on the element first.

        :param user: The user trying to update the element.
        :param element: The element that should be updated.
        :param values: The values that should be set on the element.
        :return: The updated element.
        """

        CoreHandler().check_permissions(
            user,
            UpdateElementOperationType.type,
            group=element.page.builder.group,
            context=element,
        )

        element = self.handler.update_element(element, values)

        element_updated.send(self, element=element, user=user)

        return element

    def delete_element(self, user: AbstractUser, element: Element):
        """
        Deletes an element.

        :param user: The user trying to delete the element.
        :param element: The to-be-deleted element.
        """

        page = element.page

        CoreHandler().check_permissions(
            user,
            DeleteElementOperationType.type,
            group=element.page.builder.group,
            context=element,
        )

        self.handler.delete_element(element)

        element_deleted.send(self, element_id=element.id, page=page, user=user)

    def order_elements(
        self, user: AbstractUser, page: Page, new_order: List[int]
    ) -> List[int]:
        """
        Orders the elements of a page in a new order. The user must have the permissions
        over all elements matching the given ids.

        :param user: The user trying to re-order the elements.
        :param page: The page the elements exist on.
        :param new_order: The new order which they should have.
        :return: The full order of all elements after they have been ordered.
        """

        CoreHandler().check_permissions(
            user,
            OrderElementsPageOperationType.type,
            group=page.builder.group,
            context=page,
        )

        all_elements = Element.objects.filter(page=page)

        user_elements = CoreHandler().filter_queryset(
            user,
            OrderElementsPageOperationType.type,
            all_elements,
            group=page.builder.group,
            context=page,
        )

        element_ids = set(user_elements.values_list("id", flat=True))

        # Check if all ids belong to the page and if the user has access to it
        for element_id in new_order:
            if element_id not in element_ids:
                raise ElementNotInPage(element_id)

        full_order = self.handler.order_elements(page, new_order)

        elements_reordered.send(self, page=page, order=full_order, user=user)

        return full_order
