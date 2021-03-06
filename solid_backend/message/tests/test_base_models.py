from django.db import models


class TestMessageModelExists:
    """
    Test whether an object Message can be imported and is a Django model.
    """

    def test_model_exists(self):
        pass

    def test_model_is_django_model(self):
        from solid_backend.message.models import Message

        assert issubclass(Message, models.Model)


class TestMessageModelFields:
    """
    Test suite with basic field tests whether all fields of the Message object exist and
    have the correct class instance and field attribute values.
    """

    def test_model_has_field_type(self, message_model_class):
        assert hasattr(message_model_class, "type")

    def test_model_has_field_title(self, message_model_class):
        assert hasattr(message_model_class, "title")

    def test_model_has_field_text(self, message_model_class):
        assert hasattr(message_model_class, "text")

    def test_model_has_field_img(self, message_model_class):
        assert hasattr(message_model_class, "img")

    def test_model_has_field_valid_from(self, message_model_class):
        assert hasattr(message_model_class, "valid_from")

    def test_model_has_field_valid_to(self, message_model_class):
        assert hasattr(message_model_class, "valid_to")

    def test_field_type_type(self, message_model_class):
        assert isinstance(message_model_class._meta.get_field("type"), models.CharField)

    def test_field_type_title(self, message_model_class):
        assert isinstance(
            message_model_class._meta.get_field("title"), models.CharField
        )

    def test_field_type_text(self, message_model_class):
        assert isinstance(message_model_class._meta.get_field("text"), models.TextField)

    def test_field_type_img(self, message_model_class):
        assert isinstance(message_model_class._meta.get_field("img"), models.ForeignKey)

    def test_field_type_valid_from(self, message_model_class):
        assert isinstance(
            message_model_class._meta.get_field("valid_from"), models.DateField
        )

    def test_field_type_valid_to(self, message_model_class):
        assert isinstance(
            message_model_class._meta.get_field("valid_to"), models.DateField
        )

    def test_field_attribute_values_img(
        self, message_model_class, photograph_model_class
    ):
        field = message_model_class._meta.get_field("img")
        assert issubclass(field.related_model, photograph_model_class)
