import pytest
from photograph.models import Photograph


@pytest.fixture
def photograph_model_class():
    return Photograph
