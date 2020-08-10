import pytest
from django.contrib.admin.sites import AdminSite
from django.core.files.uploadedfile import SimpleUploadedFile

from solid_backend.photograph.admin import PhotographAdmin
from solid_backend.photograph.models import Photograph

CURRENT_RELATIVE_PATH = "solid_backend/photograph/tests/conftest_files/"
test_img_filename = "{}100x100_test_img.jpg".format(CURRENT_RELATIVE_PATH)
test_audio_filename = "{}test_mp3_file.mp3".format(CURRENT_RELATIVE_PATH)


@pytest.fixture
def photograph_model_class():
    return Photograph


@pytest.fixture
def photograph_admin_form():
    return PhotographAdmin(Photograph, AdminSite()).get_form(request=None)


@pytest.fixture
def valid_photograph_data():
    data = {
        "length_value": 5.0,  # 5 cm
        "length_unit": 0.01,  # cm
        "pixel_number": 100,  # per 100 pixel
        "img_alt": "Alternative text to describe the image.",
    }
    return data


@pytest.fixture
def valid_photograph_files():
    files = {
        "img": SimpleUploadedFile(
            test_img_filename, open(test_img_filename, "rb").read()
        ),
        "audio": SimpleUploadedFile(
            test_audio_filename, open(test_audio_filename, "rb").read()
        ),
    }
    return files


@pytest.fixture
def valid_img():
    return {
        "img": SimpleUploadedFile(
            test_img_filename, open(test_img_filename, "rb").read()
        )
    }


@pytest.fixture
def photograph_object(
    photograph_admin_form, valid_photograph_data, valid_photograph_files
):
    form = photograph_admin_form(valid_photograph_data, valid_photograph_files)
    form.is_valid()
    instance = form.save()
    return instance
