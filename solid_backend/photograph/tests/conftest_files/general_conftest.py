import pytest

from solid_backend.photograph.models import DeepZoom, Photograph


@pytest.fixture
def deepzoom_model_class():
    return DeepZoom


@pytest.fixture
def photograph_model_class():
    return Photograph
