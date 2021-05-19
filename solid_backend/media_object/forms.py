from django import forms
from django.contrib.contenttypes.forms import BaseGenericInlineFormSet
from mutagen import File
from django.core.validators import FileExtensionValidator
from django.utils.translation import ugettext_lazy as _


def validate_media_object_file_extensions(value):
    return FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "mp3", "mp4"])(value)


class MediaObjectFormField(forms.FileField):
    """
    Form field to accept jpg, jpeg, mp3 and mp4 files.
    """
    default_validators = [validate_media_object_file_extensions,]


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


# Field Lists for validating the MediaObjectForm
GENERAL_FIELDS = [
    "media_format",
    "file",
    "title",
    "description",
    "date",
    "author",
    "license",
]

# length_unit is missing from this list since it always has a non-False default anyways
IMG_FIELDS = [
    "dzi_option",
    "img_alt",
    "dzi_file",
    "img_original_width",
    "img_original_height",
    ("length_value", "length_unit", "pixel_number"),
    "img_original_scale",
    "audio",
    "audio_duration",
    "length_value",
    "pixel_number",
]
AUDIO_VIDEO_FIELDS = ["media_duration", ]


class MediaObjectAdminForm(forms.ModelForm):
    """
    Calculate the scale and determine the audio duration.
    """
    media_format = forms.ChoiceField(
        choices=(
            ("image", _("image")),
            ("audio", _("audio")),
            ("video", _("video")),
        ),
        widget=forms.RadioSelect()
    )
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

    def clean(self):
        """
        Validate whether fields for not matching media_formats were submitted.
        :return:
        """
        cleaned_data = super(MediaObjectAdminForm, self).clean()

        if cleaned_data["media_format"] == "image":
            if any(cleaned_data.get(x, False) for x in AUDIO_VIDEO_FIELDS):
                raise forms.ValidationError(_("You submitted value(s) for field(s) which are not supported for the media_format image."))
        else:
            if any(cleaned_data.get(x, False) for x in IMG_FIELDS):
                raise forms.ValidationError(_("You submitted value(s) for field(s) which are not supported for the media_format audio/video."))
