import pytest

from solid_backend.message.models import Message
from solid_backend.photograph.models import Photograph


@pytest.fixture
def message_model_class():
    return Message


@pytest.fixture
def photograph_model_class():
    return Photograph
