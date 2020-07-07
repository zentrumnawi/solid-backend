from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from .forms import PhotographForm
from .models import Photograph


class PhotographInline(GenericTabularInline):
    model = Photograph


class PhotographAdmin(admin.ModelAdmin):
    form = PhotographForm
    fields = [
        "img",
        ("length_value", "length_unit", "pixel_number"),
        "img_alt",
        "description",
        "audio",
        "date",
        "author",
        "license",
    ]
    list_display = ["id", "img", "img_original_scale", "author"]


admin.site.register(Photograph, PhotographAdmin)
