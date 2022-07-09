import pytest
import stripe

from poc_django_stripe.users.models import User
from poc_django_stripe.users.tests.factories import UserFactory


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def user() -> User:
    return UserFactory()


@pytest.fixture(autouse=True)
def setup_stripe():
    orig_attrs = {
        "api_base": stripe.api_base,
        "api_key": stripe.api_key,
        "client_id": stripe.client_id,
        "default_http_client": stripe.default_http_client,
    }
    http_client = stripe.http_client.new_default_http_client()
    stripe.api_base = "http://localhost:%s" % 12111
    stripe.api_key = "sk_test_123"
    stripe.client_id = "ca_123"
    stripe.default_http_client = http_client
    yield
    http_client.close()
    stripe.api_base = orig_attrs["api_base"]
    stripe.api_key = orig_attrs["api_key"]
    stripe.client_id = orig_attrs["client_id"]
    stripe.default_http_client = orig_attrs["default_http_client"]
