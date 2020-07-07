import pytest

from solid_backend.slideshow.models import Slideshow, SlideshowImage, SlideshowPage


@pytest.fixture
def slideshow_model_class():
    return Slideshow


@pytest.fixture
def slideshow_page_model_class():
    return SlideshowPage


@pytest.fixture
def slideshow_image_model_class():
    return SlideshowImage
