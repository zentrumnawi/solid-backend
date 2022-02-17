from django.contrib import admin

from solid_backend.media_object.admin import (
    AudioVideoMediaObjectInline,
    ImageMediaObjectInline,
)

from .models import SampleProfile, SecondSampleProfile


class SampleProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "tree_node")
    list_display_links = ("name",)

    inlines = [ImageMediaObjectInline, AudioVideoMediaObjectInline]


admin.site.register(SampleProfile, SampleProfileAdmin)


class SecondSampleProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "tree_node")
    list_display_links = ("name",)

    inlines = [ImageMediaObjectInline, AudioVideoMediaObjectInline]


admin.site.register(SecondSampleProfile, SecondSampleProfileAdmin)
