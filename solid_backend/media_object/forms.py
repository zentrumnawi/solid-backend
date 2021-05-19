from django import forms
from django.contrib.contenttypes.forms import BaseGenericInlineFormSet
from mutagen import File

from .models import MediaObject


class MediaObjectInlineFormSet(BaseGenericInlineFormSet):
    """
    Validate if profile position is available and order froms by profile position.
    """

    def clean(self):
        super().clean()

        positions = []

        for form in self.forms:
            if form.cleaned_data.get("DELETE"):
                continue
            position = form.cleaned_data.get("profile_position")
            if not position:
                continue
            positions.append(position)

            if positions.count(position) > 1:
                form.add_error("profile_position", "This position is not available.")

    def get_queryset(self):
        return super().get_queryset().order_by("profile_position")


class MediaObjectAdminForm(forms.ModelForm):
    """
    Calculate the scale and determine the audio duration.
    """

    LENGTH_UNIT_CHOICES = [
        (1.00, "m"),
        (0.01, "cm"),
        (0.001, "mm"),
    ]
    length_value = forms.FloatField(
        min_value=0.001,
        required=False,
        label="Scale calculator",
        help_text="Längenwert",
    )
    length_unit = forms.TypedChoiceField(
        coerce=float,
        choices=LENGTH_UNIT_CHOICES,
        initial=LENGTH_UNIT_CHOICES[1][0],
        label="",
        help_text="Längeneinheit",
    )
    pixel_number = forms.IntegerField(
        max_value=32767,
        min_value=0,
        required=False,
        label="",
        help_text='Pixelanzahl ("0" löscht den Wert von Scale)',
    )

    def save(self, commit=True):
        length_value = self.cleaned_data.get("length_value")
        length_unit = self.cleaned_data.get("length_unit")
        pixel_number = self.cleaned_data.get("pixel_number")

        instance = super(MediaObjectAdminForm, self).save(commit=False)

        if length_value and pixel_number:
            instance.img_original_scale = length_value * length_unit / pixel_number

        if pixel_number == 0:
            instance.img_original_scale = None

        if instance.audio:
            instance.audio_duration = File(instance.audio).info.length
        else:
            instance.audio_duration = None

        if commit:
            instance.save()

        return instance
