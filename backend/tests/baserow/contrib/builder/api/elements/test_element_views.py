from django.urls import reverse

import pytest
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
)


@pytest.mark.django_db
def test_create_element(api_client, data_fixture):
    user, token = data_fixture.create_user_and_token()
    page = data_fixture.create_builder_page(user=user)

    url = reverse("api:builder:element:list", kwargs={"page_id": page.id})
    response = api_client.post(
        url,
        {"type": "heading"},
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )

    response_json = response.json()
    assert response.status_code == HTTP_200_OK
    assert response_json["type"] == "heading"


@pytest.mark.django_db
def test_create_element_permission_denied(
    api_client, data_fixture, stub_check_permissions
):
    user, token = data_fixture.create_user_and_token()
    page = data_fixture.create_builder_page(user=user)

    url = reverse("api:builder:element:list", kwargs={"page_id": page.id})
    with stub_check_permissions(raise_permission_denied=True):
        response = api_client.post(
            url,
            {"type": "heading"},
            format="json",
            HTTP_AUTHORIZATION=f"JWT {token}",
        )

    assert response.status_code == HTTP_401_UNAUTHORIZED
    assert response.json()["error"] == "PERMISSION_DENIED"


@pytest.mark.django_db
def test_create_element_page_does_not_exist(api_client, data_fixture):
    user, token = data_fixture.create_user_and_token()

    url = reverse("api:builder:element:list", kwargs={"page_id": 0})
    response = api_client.post(
        url,
        {"type": "heading"},
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )

    assert response.status_code == HTTP_404_NOT_FOUND
    assert response.json()["error"] == "ERROR_PAGE_DOES_NOT_EXIST"


@pytest.mark.django_db
def test_update_element(api_client, data_fixture):
    user, token = data_fixture.create_user_and_token()
    page = data_fixture.create_builder_page(user=user)
    element1 = data_fixture.create_builder_header_element(page=page)

    url = reverse("api:builder:element:item", kwargs={"element_id": element1.id})
    response = api_client.patch(
        url,
        {"config": {"value": "unusual value"}},
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    assert response.status_code == HTTP_200_OK
    assert response.json()["config"] == {"value": "unusual value"}


@pytest.mark.django_db
def test_update_element_does_not_exist(api_client, data_fixture):
    user, token = data_fixture.create_user_and_token()

    url = reverse("api:builder:element:item", kwargs={"element_id": 0})
    response = api_client.patch(
        url,
        {"config": {"value": "unusual value"}},
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    assert response.status_code == HTTP_404_NOT_FOUND
    assert response.json()["error"] == "ERROR_ELEMENT_DOES_NOT_EXIST"


@pytest.mark.django_db
def test_order_elements(api_client, data_fixture):
    user, token = data_fixture.create_user_and_token()
    page = data_fixture.create_builder_page(user=user)
    element1 = data_fixture.create_builder_header_element(page=page)
    element2 = data_fixture.create_builder_header_element(page=page)
    element3 = data_fixture.create_builder_header_element(page=page)

    url = reverse("api:builder:element:order", kwargs={"page_id": page.id})
    response = api_client.post(
        url,
        {"element_ids": [element3.id, element1.id]},
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )

    assert response.status_code == HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_order_elements_element_not_in_page(api_client, data_fixture):
    user, token = data_fixture.create_user_and_token()
    page = data_fixture.create_builder_page(user=user)
    element1 = data_fixture.create_builder_header_element(page=page)
    element2 = data_fixture.create_builder_header_element(page=page)
    element3 = data_fixture.create_builder_header_element(user=user)

    url = reverse("api:builder:element:order", kwargs={"page_id": page.id})
    response = api_client.post(
        url,
        {"element_ids": [element3.id, element1.id]},
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )

    assert response.status_code == HTTP_400_BAD_REQUEST
    assert response.json()["error"] == "ERROR_ELEMENT_NOT_IN_PAGE"


@pytest.mark.django_db
def test_order_elements_page_does_not_exist(api_client, data_fixture):
    user, token = data_fixture.create_user_and_token()
    page = data_fixture.create_builder_page(user=user)
    element1 = data_fixture.create_builder_header_element(page=page)
    element2 = data_fixture.create_builder_header_element(page=page)
    element3 = data_fixture.create_builder_header_element(user=user)

    url = reverse("api:builder:element:order", kwargs={"page_id": 0})
    response = api_client.post(
        url,
        {"element_ids": [element3.id, element1.id]},
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )

    assert response.status_code == HTTP_404_NOT_FOUND
    assert response.json()["error"] == "ERROR_PAGE_DOES_NOT_EXIST"


@pytest.mark.django_db
def test_delete_element(api_client, data_fixture):
    user, token = data_fixture.create_user_and_token()
    page = data_fixture.create_builder_page(user=user)
    element1 = data_fixture.create_builder_header_element(page=page)

    url = reverse("api:builder:element:item", kwargs={"element_id": element1.id})
    response = api_client.delete(
        url,
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )
    assert response.status_code == HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_delete_element_permission_denied(
    api_client, data_fixture, stub_check_permissions
):
    user, token = data_fixture.create_user_and_token()
    page = data_fixture.create_builder_page(user=user)
    element1 = data_fixture.create_builder_header_element(page=page)

    url = reverse("api:builder:element:item", kwargs={"element_id": element1.id})

    with stub_check_permissions(raise_permission_denied=True):
        response = api_client.delete(
            url,
            format="json",
            HTTP_AUTHORIZATION=f"JWT {token}",
        )

    assert response.status_code == HTTP_401_UNAUTHORIZED
    assert response.json()["error"] == "PERMISSION_DENIED"


@pytest.mark.django_db
def test_delete_element_element_not_exist(api_client, data_fixture):
    user, token = data_fixture.create_user_and_token()

    url = reverse("api:builder:element:item", kwargs={"element_id": 0})
    response = api_client.delete(
        url,
        format="json",
        HTTP_AUTHORIZATION=f"JWT {token}",
    )

    assert response.status_code == HTTP_404_NOT_FOUND
    assert response.json()["error"] == "ERROR_ELEMENT_DOES_NOT_EXIST"
