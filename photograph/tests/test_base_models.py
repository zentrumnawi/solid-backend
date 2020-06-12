import pytest
from django.db import models


class TestPhotographModelExists:
    """
    Test whether an object Phtotograph can be imported and is a Django model.
    """

    def test_model_exists(self):
        from photograph.models import Photograph

    def test_model_is_django_model(self):
        from photograph.models import Photograph

        assert issubclass(Photograph, models.Model)
