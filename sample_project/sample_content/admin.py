from django.contrib import admin

from solid_backend.photograph.admin import PhotographInline

from .models import SampleProfile


class SampleProfileAdmin(admin.ModelAdmin):
    inlines = [
        PhotographInline,
    ]


admin.site.register(SampleProfile, SampleProfileAdmin)
