import pytest

from baserow.contrib.builder.elements.registries import (
    ElementType,
    element_type_registry,
)


def pytest_generate_tests(metafunc):
    if "element_type" in metafunc.fixturenames:
        metafunc.parametrize(
            "element_type",
            [pytest.param(e, id=e.type) for e in element_type_registry.get_all()],
        )


@pytest.mark.django_db
def test_export_element(data_fixture, element_type: ElementType):
    page = data_fixture.create_builder_page()
    sample_params = element_type.get_sample_params()
    element = data_fixture.create_builder_element(
        element_type.model_class, page=page, order=17, **sample_params
    )

    exported = element_type.export_serialized(element)

    assert exported["id"] == element.id
    assert exported["type"] == element_type.type
    assert exported["order"] == element.order

    for key, value in sample_params.items():
        assert exported[key] == value


@pytest.mark.django_db
def test_import_element(data_fixture, element_type: ElementType):
    page = data_fixture.create_builder_page()
    sample_params = element_type.get_sample_params()

    serialized = {"id": 9999, "order": 42, "type": element_type.type}
    serialized.update(element_type.get_sample_params())

    id_mapping = {}
    element = element_type.import_serialized(page, serialized, id_mapping)

    assert element.id != 9999
    assert element.order == element.order
    assert isinstance(element, element_type.model_class)

    for key, value in sample_params.items():
        assert getattr(element, key) == value
