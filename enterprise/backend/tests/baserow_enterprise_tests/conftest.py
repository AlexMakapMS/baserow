from django.test.utils import override_settings

from baserow_premium.license.exceptions import LicenseAlreadyExistsError
from baserow_premium.license.handler import LicenseHandler

from baserow.core.models import Settings

# noinspection PyUnresolvedReferences
from baserow.test_utils.pytest_conftest import *  # noqa: F403, F401

VALID_ONE_SEAT_ENTERPRISE_LICENSE = (
    # id: "1", instance_id: "1"
    b"eyJ2ZXJzaW9uIjogMSwgImlkIjogIjUzODczYmVkLWJlNTQtNDEwZS04N2EzLTE2OTM2ODY2YjBiNiIsICJ2YWxpZF9mcm9tIjogIjIwMjItMTAtMDFUMDA6MDA6MDAiLCAidmFsaWRfdGhyb3VnaCI6ICIyMDY5LTA4LTA5VDIzOjU5OjU5IiwgInByb2R1Y3RfY29kZSI6ICJlbnRlcnByaXNlIiwgInNlYXRzIjogMSwgImlzc3VlZF9vbiI6ICIyMDIyLTEwLTI2VDE0OjQ4OjU0LjI1OTQyMyIsICJpc3N1ZWRfdG9fZW1haWwiOiAidGVzdEB0ZXN0LmNvbSIsICJpc3N1ZWRfdG9fbmFtZSI6ICJ0ZXN0QHRlc3QuY29tIiwgImluc3RhbmNlX2lkIjogIjEifQ==.B7aPXR0R4Fxr28AL7B5oopa2Yiz_MmEBZGdzSEHHLt4wECpnzjd_SF440KNLEZYA6WL1rhNkZ5znbjYIp6KdCqLdcm1XqNYOIKQvNTOtl9tUAYj_Qvhq1jhqSja-n3HFBjIh9Ve7a6T1PuaPLF1DoxSRGFZFXliMeJRBSzfTsiHiO22xRQ4GwafscYfUIWvIJJHGHtYEd9rk0tG6mfGEaQGB4e6KOsN-zw-bgLDBOKmKTGrVOkZnaGHBVVhUdpBn25r3CFWqHIApzUCo81zAA96fECHPlx_fBHhvIJXLsN5i3LdeJlwysg5SBO15Vt-tsdPmdcsec-fOzik-k3ib0A== "
)


@pytest.fixture  # noqa: F405
def enterprise_data_fixture(data_fixture):
    from .fixtures import EnterpriseFixtures

    class EnterpriseFixtures(EnterpriseFixtures, data_fixture.__class__):
        def enable_enterprise(self):
            Settings.objects.update_or_create(defaults={"instance_id": "1"})
            user = data_fixture.create_user(is_staff=True)
            try:
                LicenseHandler.register_license(user, VALID_ONE_SEAT_ENTERPRISE_LICENSE)
            except LicenseAlreadyExistsError:
                pass

    return EnterpriseFixtures()


@pytest.fixture  # noqa: F405
def enable_enterprise(db, enterprise_data_fixture):
    with override_settings(DEBUG=True):
        enterprise_data_fixture.enable_enterprise()
        yield
