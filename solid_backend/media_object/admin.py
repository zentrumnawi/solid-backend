from django.contrib import admin, messages
from django.contrib.contenttypes.admin import GenericTabularInline
from django.utils.translation import ugettext_lazy as _

from .forms import (
    GENERAL_FIELDS_1,
    GENERAL_FIELDS_2,
    IMG_FIELDS,
    IMG_FIELDS_1,
    IMG_FIELDS_2,
    AudioVideoMediaObjectForm,
    ImageMediaObjectForm,
    MediaObjectAdminForm,
    MediaObjectInlineFormSet,
)
from .models import AudioVideoMediaObject, ImageMediaObject, MediaObject

fields = [
    "profile_position",
    # Data
    "media_format",
    ("file", "dzi_option"),
    "title",
    # Fields for "image" selected
    "img_alt",
    "dzi_file",
    "img_original_width",
    "img_original_height",
    ("length_value", "length_unit", "pixel_number"),
    "img_original_scale",
    "audio",
    "description",
    "date",
    "author",
    "license",
]
readonly_fields = [
    "dzi_file",
    "img_original_width",
    "img_original_height",
    "img_original_scale",
]


class DeepZoomAdmin(admin.ModelAdmin):
    actions = ["switch_dzi_option"]

    def delete_queryset(self, request, queryset):
        # Call DeepZoom model delete method for each selected object during bulk delete
        # via admin action to ensure that the Deep Zoom directory trees will be deleted.
        for obj in queryset:
            obj.delete()

    def switch_dzi_option(self, request, queryset):
        # Switch the Deep Zoom option for each selected object and either create or
        # delete its Deep Zoom image files.
        for obj in queryset:
            if not obj.dzi_option:
                obj.dzi_option = True
            else:
                obj.dzi_option = False
            obj.save()

        n = queryset.count()

        self.message_user(
            request,
            "Successfully switched Deep Zoom option on {} {}.".format(
                n, admin.utils.model_ngettext(self.opts, n)
            ),
            messages.SUCCESS,
        )

    switch_dzi_option.short_description = (
        "Switch Deep Zoom option on selected photographs"
    )


class MediaObjectInline(GenericTabularInline):
    model = MediaObject
    form = MediaObjectAdminForm
    formset = MediaObjectInlineFormSet
    extra = 1
    fields = fields
    readonly_fields = readonly_fields


class ImageMediaObjectInline(GenericTabularInline):
    model = ImageMediaObject
    form = ImageMediaObjectForm
    formset = MediaObjectInlineFormSet
    extra = 1
    fields = GENERAL_FIELDS_1 + IMG_FIELDS_1 + GENERAL_FIELDS_2 + IMG_FIELDS_2
    readonly_fields = readonly_fields

    verbose_name = _("Image")
    verbose_name_plural = _("Images")


class AudioVideoMediaObjectInline(GenericTabularInline):
    model = AudioVideoMediaObject
    form = AudioVideoMediaObjectForm
    formset = MediaObjectInlineFormSet
    extra = 1
    fields = GENERAL_FIELDS_1 + GENERAL_FIELDS_2
    readonly_fields = readonly_fields

    verbose_name = _("Audio/Video")
    verbose_name_plural = _("Audios and Videos")


class MediaObjectAdmin(DeepZoomAdmin):
    form = MediaObjectAdminForm
    fields = ["profile"] + fields
    readonly_fields = ["profile", "profile_position"] + readonly_fields
    list_display = ["id", "profile", "dzi_option", "author", "license"]

    def profile(self, obj):
        if not obj.profile:
            return "-"
        return str(obj.profile)

    class Media:
        js = (
            "//ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js",
            "media_object/js/hide_elements.js",
        )
        css = {
            "all": ("media_object/css/radio.css",),
        }


admin.site.register(MediaObject, MediaObjectAdmin)
