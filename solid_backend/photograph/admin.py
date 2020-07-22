from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from .forms import PhotographForm
from .models import Photograph


class PhotographInline(GenericTabularInline):
    model = Photograph
    form = PhotographForm
    extra = 1
    fields = [
        "img",
        "img_alt",
        "description",
        ("length_value", "length_unit", "pixel_number"),
        "audio",
        "date",
        "author",
        "license",
    ]


class PhotographAdmin(admin.ModelAdmin):
    form = PhotographForm
    fields = [
        "img",
        "img_alt",
        "description",
        ("length_value", "length_unit", "pixel_number"),
        "audio",
        "date",
        "author",
        "license",
    ]
    list_display = ["id", "img", "img_original_scale", "author"]


admin.site.register(Photograph, PhotographAdmin)
