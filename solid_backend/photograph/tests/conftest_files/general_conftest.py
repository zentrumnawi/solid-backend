import pytest

from solid_backend.photograph.models import Photograph


@pytest.fixture
def photograph_model_class():
    return Photograph
