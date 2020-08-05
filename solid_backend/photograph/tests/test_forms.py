import pytest
from django import forms


class TestPhotographModelForm:
    def test_photograph_admin_form_exists(self):
        from solid_backend.photograph.forms import PhotographForm

    def test_form_has_length_value_field(self, photograph_admin_form):
        field = photograph_admin_form.base_fields.get("length_value")
        assert field
        assert isinstance(field, forms.FloatField)

    def test_form_has_length_unit_field(self, photograph_admin_form):
        field = photograph_admin_form.base_fields.get("length_unit")
        assert field
        assert isinstance(field, forms.TypedChoiceField)

    def test_form_has_pixel_number_field(self, photograph_admin_form):
        field = photograph_admin_form.base_fields.get("pixel_number")
        assert field
        assert isinstance(field, forms.IntegerField)

    def test_form_has_unit_choices(self, photograph_admin_form):
        assert hasattr(photograph_admin_form, "LENGTH_UNIT_CHOICES")

        choices = [
            (1.00, "m"),
            (0.01, "cm"),
            (0.001, "mm"),
        ]

        assert photograph_admin_form.LENGTH_UNIT_CHOICES == choices

    @pytest.mark.django_db
    def test_audio_file_duration(self, photograph_object):
        assert photograph_object.audio_duration == 2.0

    @pytest.mark.django_db
    def test_scale_factor_calculation(self, photograph_object):
        assert photograph_object.img_original_scale == 5e-4

    @pytest.mark.django_db
    def test_delete_scale_factor(
        self, valid_photograph_data, photograph_object, photograph_admin_form
    ):
        valid_photograph_data["pixel_number"] = 0
        form = photograph_admin_form(valid_photograph_data, instance=photograph_object)
        form.is_valid()
        instance = form.save()

        assert instance.img_original_scale is None

    @pytest.mark.django_db
    def test_audio_duration_without_file(
        self, photograph_object, valid_photograph_data, valid_img, photograph_admin_form
    ):

        form = photograph_admin_form(
            valid_photograph_data, files={"audio": False}, instance=photograph_object
        )
        form.is_valid()
        instance = form.save()

        assert not instance.audio
        assert instance.audio_duration is None
