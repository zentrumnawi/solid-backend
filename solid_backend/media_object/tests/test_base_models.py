from django.db import models
from stdimage import JPEGField


class TestDeepZoomModelExists:
    """
    Test whether an object DeepZoom can be imported and is a Django model.
    """

    def test_model_exists(self):
        pass

    def test_model_is_django_model(self):
        from solid_backend.photograph.models import DeepZoom

        assert issubclass(DeepZoom, models.Model)


class TestDeepZoomModelFields:
    """
    Test suite with basic field tests whether all fields of the DeepZoom
    object exist and have the correct class instance.
    """

    def test_model_has_field_dzi_option(self, deepzoom_model_class):
        assert hasattr(deepzoom_model_class, "dzi_option")

    def test_model_has_field_dzi_file(self, deepzoom_model_class):
        assert hasattr(deepzoom_model_class, "dzi_file")

    def test_field_type_dzi_option(self, deepzoom_model_class):
        assert isinstance(
            deepzoom_model_class._meta.get_field("dzi_option"), models.BooleanField
        )

    def test_field_type_dzi_file(self, deepzoom_model_class):
        assert isinstance(
            deepzoom_model_class._meta.get_field("dzi_file"), models.FileField
        )


class TestPhotographModelExists:
    """
    Test whether an object Photograph can be imported and is a Django model.
    """

    def test_model_exists(self):
        pass

    def test_model_is_django_model(self):
        from solid_backend.media_object.models import MediaObject

        assert issubclass(MediaObject, models.Model)


class TestPhotographModelFields:
    """
    Test suite with basic field tests whether all fields of the Photograph
    object exist and have the correct class instance.
    """

    def test_model_has_field_img(self, media_object_model_class):
        assert hasattr(media_object_model_class, "img")

    def test_model_has_field_img_original_width(self, media_object_model_class):
        assert hasattr(media_object_model_class, "img_original_width")

    def test_model_has_field_img_original_height(self, media_object_model_class):
        assert hasattr(media_object_model_class, "img_original_height")

    def test_model_has_field_img_original_scale(self, media_object_model_class):
        assert hasattr(media_object_model_class, "img_original_scale")

    def test_model_has_field_img_alt(self, media_object_model_class):
        assert hasattr(media_object_model_class, "img_alt")

    def test_model_has_field_description(self, media_object_model_class):
        assert hasattr(media_object_model_class, "description")

    def test_model_has_field_audio(self, media_object_model_class):
        assert hasattr(media_object_model_class, "audio")

    def test_model_has_field_audio_duration(self, media_object_model_class):
        assert hasattr(media_object_model_class, "audio_duration")

    def test_model_has_field_profile_position(self, media_object_model_class):
        assert hasattr(media_object_model_class, "profile_position")

    def test_model_has_field_date(self, media_object_model_class):
        assert hasattr(media_object_model_class, "date")

    def test_model_has_field_author(self, media_object_model_class):
        assert hasattr(media_object_model_class, "author")

    def test_model_has_field_license(self, media_object_model_class):
        assert hasattr(media_object_model_class, "license")

    def test_field_type_img(self, media_object_model_class):
        assert isinstance(media_object_model_class._meta.get_field("img"), JPEGField)

    def test_field_type_img_original_width(self, media_object_model_class):
        assert isinstance(
            media_object_model_class._meta.get_field("img_original_width"),
            models.PositiveSmallIntegerField,
        )

    def test_field_type_img_original_height(self, media_object_model_class):
        assert isinstance(
            media_object_model_class._meta.get_field("img_original_height"),
            models.PositiveSmallIntegerField,
        )

    def test_field_type_img_original_scale(self, media_object_model_class):
        assert isinstance(
            media_object_model_class._meta.get_field("img_original_scale"),
            models.FloatField,
        )

    def test_field_type_img_alt(self, media_object_model_class):
        assert isinstance(
            media_object_model_class._meta.get_field("img_alt"), models.CharField
        )

    def test_field_type_description(self, media_object_model_class):
        assert isinstance(
            media_object_model_class._meta.get_field("description"), models.TextField
        )

    def test_field_type_audio(self, media_object_model_class):
        assert isinstance(
            media_object_model_class._meta.get_field("audio"), models.FileField
        )

    def test_field_type_audio_duration(self, media_object_model_class):
        assert isinstance(
            media_object_model_class._meta.get_field("audio_duration"),
            models.FloatField,
        )

    def test_field_type_profile_position(self, media_object_model_class):
        assert isinstance(
            media_object_model_class._meta.get_field("profile_position"),
            models.PositiveSmallIntegerField,
        )

    def test_field_type_date(self, media_object_model_class):
        assert isinstance(
            media_object_model_class._meta.get_field("date"), models.DateField
        )

    def test_field_type_author(self, media_object_model_class):
        assert isinstance(
            media_object_model_class._meta.get_field("author"), models.CharField
        )

    def test_field_type_license(self, media_object_model_class):
        assert isinstance(
            media_object_model_class._meta.get_field("license"), models.CharField
        )
