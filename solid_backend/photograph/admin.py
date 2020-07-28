from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from .forms import PhotographForm
from .models import Photograph

fields = [
    "img",
    "img_alt",
    "description",
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
    "img_original_width",
    "img_original_height",
    "img_original_scale",
    "audio_duration",
]


class PhotographInline(GenericTabularInline):
    model = Photograph
    form = PhotographForm
    extra = 1
    fields = fields
    readonly_fields = readonly_fields


class PhotographAdmin(admin.ModelAdmin):
    form = PhotographForm
    fields = fields
    readonly_fields = readonly_fields
    list_display = ["id", "img", "author", "license"]


admin.site.register(Photograph, PhotographAdmin)
