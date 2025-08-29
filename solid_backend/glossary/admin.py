from django.contrib import admin
from django import forms
from django.conf import settings
from .forms import GlossaryEntryAdminForm
from .models import GlossaryEntry


class GlossaryEntryAdmin(admin.ModelAdmin):
    form = GlossaryEntryAdminForm
    list_display = ["id", "term"]

    def get_exclude(self, request, obj=None):
        if not GlossaryEntryAdminForm.should_show_tags(self):
            return ("tags",)
        return []


admin.site.register(GlossaryEntry, GlossaryEntryAdmin)
