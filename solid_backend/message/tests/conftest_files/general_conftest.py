import pytest

from solid_backend.message.models import Message


@pytest.fixture
def message_model_class():
    return Message
