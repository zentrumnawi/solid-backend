from django.db import models
from stdimage import JPEGField


class TestPhotographModelExists:
    """
    Test whether an object Phtotograph can be imported and is a Django model.
    """

    def test_model_exists(self):
        pass

    def test_model_is_django_model(self):
        from solid_backend.photograph.models import Photograph

        assert issubclass(Photograph, models.Model)


class TestPhotographModelFields:
    """
    Test suite with basic field tests whether all fields of the Photograph
    object exist and have the correct class instance.
    """

    def test_model_has_field_img(self, photograph_model_class):
        assert hasattr(photograph_model_class, "img")

    def test_model_has_field_img_original_width(self, photograph_model_class):
        assert hasattr(photograph_model_class, "img_original_width")

    def test_model_has_field_img_original_height(self, photograph_model_class):
        assert hasattr(photograph_model_class, "img_original_height")

    def test_model_has_field_img_original_scale(self, photograph_model_class):
        assert hasattr(photograph_model_class, "img_original_scale")

    def test_model_has_field_img_alt(self, photograph_model_class):
        assert hasattr(photograph_model_class, "img_alt")

    def test_model_has_field_description(self, photograph_model_class):
        assert hasattr(photograph_model_class, "description")

    def test_model_has_field_audio(self, photograph_model_class):
        assert hasattr(photograph_model_class, "audio")

    def test_model_has_field_audio_duration(self, photograph_model_class):
        assert hasattr(photograph_model_class, "audio_duration")

    def test_model_has_field_date(self, photograph_model_class):
        assert hasattr(photograph_model_class, "date")

    def test_model_has_field_author(self, photograph_model_class):
        assert hasattr(photograph_model_class, "author")

    def test_model_has_field_license(self, photograph_model_class):
        assert hasattr(photograph_model_class, "license")

    def test_field_type_img(self, photograph_model_class):
        assert isinstance(photograph_model_class._meta.get_field("img"), JPEGField)

    def test_field_type_img_original_width(self, photograph_model_class):
        assert isinstance(
            photograph_model_class._meta.get_field("img_original_width"),
            models.PositiveSmallIntegerField,
        )

    def test_field_type_img_original_height(self, photograph_model_class):
        assert isinstance(
            photograph_model_class._meta.get_field("img_original_height"),
            models.PositiveSmallIntegerField,
        )

    def test_field_type_img_original_scale(self, photograph_model_class):
        assert isinstance(
            photograph_model_class._meta.get_field("img_original_scale"),
            models.FloatField,
        )

    def test_field_type_img_alt(self, photograph_model_class):
        assert isinstance(
            photograph_model_class._meta.get_field("img_alt"), models.CharField
        )

    def test_field_type_description(self, photograph_model_class):
        assert isinstance(
            photograph_model_class._meta.get_field("description"), models.TextField
        )

    def test_field_type_audio(self, photograph_model_class):
        assert isinstance(
            photograph_model_class._meta.get_field("audio"), models.FileField
        )

    def test_field_type_audio_duration(self, photograph_model_class):
        assert isinstance(
            photograph_model_class._meta.get_field("audio_duration"), models.FloatField
        )

    def test_field_type_date(self, photograph_model_class):
        assert isinstance(
            photograph_model_class._meta.get_field("date"), models.DateField
        )

    def test_field_type_author(self, photograph_model_class):
        assert isinstance(
            photograph_model_class._meta.get_field("author"), models.CharField
        )

    def test_field_type_license(self, photograph_model_class):
        assert isinstance(
            photograph_model_class._meta.get_field("license"), models.CharField
        )
