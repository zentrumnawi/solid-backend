from django.contrib import admin

from .forms import GlossaryEntryAdminForm
from .models import GlossaryEntry


class GlossaryEntryAdmin(admin.ModelAdmin):
    form = GlossaryEntryAdminForm
    list_display = ["id", "term"]


admin.site.register(GlossaryEntry, GlossaryEntryAdmin)
