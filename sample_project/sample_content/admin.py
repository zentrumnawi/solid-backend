from django.contrib import admin

from solid_backend.photograph.admin import PhotographInline
from solid_backend.media_object.admin import MediaObjectInline

from .models import SampleProfile


class SampleProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "tree_node")
    list_display_links = ("name",)
    inlines = [MediaObjectInline]


admin.site.register(SampleProfile, SampleProfileAdmin)
