import pytest


class TestPhotographModelForm:
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
        print(form.errors)
        instance = form.save()

        assert instance.img_original_scale == None
