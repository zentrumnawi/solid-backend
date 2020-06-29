import pytest
from solid_backend.contact.serializers import ContactSerializer


@pytest.fixture
def contact_serializer_field_dict():
    return ContactSerializer().get_fields()
