from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from .forms import PhotographForm
from .models import Photograph

fields = ["profile_position",
    ("img", "dzi_option"),
    "img_alt",
    "description",
    "dzi_file",
    "img_original_width",
    "img_original_height",
    ("length_value", "length_unit", "pixel_number"),
    "img_original_scale",
    "audio",
    "audio_duration",
    "date",
    "author",
    "license",
]
readonly_fields = [
    "dzi_file",
    "img_original_width",
    "img_original_height",
    "img_original_scale",
    "audio_duration",
]


class DeepZoomAdmin(admin.ModelAdmin):
    def delete_queryset(self, request, queryset):
        """
        Call DeepZoom model delete method for each object during bulk delete via admin
        action to ensure that the Deep Zoom directory trees will be deleted.
        """

        for object in queryset:
            object.delete()


class PhotographInline(GenericTabularInline):
    model = Photograph
    form = PhotographForm
    extra = 1
    fields = fields
    readonly_fields = readonly_fields


class PhotographAdmin(DeepZoomAdmin):
    form = PhotographForm
    fields = ["profile"] + fields
    readonly_fields = [ "profile", "profile_position"] + readonly_fields
    list_display = ["id", "profile", "img", "dzi_option", "author", "license"]

    def profile(self, obj):
        if not obj.profile:
            return "-"
        return str(obj.profile)


admin.site.register(Photograph, PhotographAdmin)
