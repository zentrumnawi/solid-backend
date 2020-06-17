from django.contrib import admin
from .models import Photograph
from .forms import PhotographForm


class PhotographAdmin(admin.ModelAdmin):
    form = PhotographForm
    fields = [
        "img",
        ("length_value", "length_unit", "pixel_number"),
        "img_alt",
        "description",
        "date",
        "author",
        "license",
    ]
    list_display = ["id", "img", "img_original_scale", "author"]


admin.site.register(Photograph, PhotographAdmin)
