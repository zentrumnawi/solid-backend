from django import forms
from .models import Photograph


class PhotographForm(forms.ModelForm):
    """
    Calculation of the scale is provided.
    """

    LENGHT_UNIT_CHOICES = [
        (1.00, "m"),
        (0.01, "cm"),
        (0.001, "mm"),
    ]
    length_value = forms.FloatField(
        min_value=0.000001, required=False, label="Scale", help_text="Längenwert",
    )
    length_unit = forms.TypedChoiceField(
        coerce=float,
        choices=LENGHT_UNIT_CHOICES,
        initial=LENGHT_UNIT_CHOICES[1][0],
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

        instance = super(PhotographForm, self).save(commit=commit)

        if length_value and pixel_number:
            instance.img_original_scale = length_value * length_unit / pixel_number

        if pixel_number == 0:
            instance.img_original_scale = None

        if commit:
            instance.save()

        return instance
