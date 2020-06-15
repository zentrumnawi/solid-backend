from django.contrib import admin
from .models import Photograph


class PhotographAdmin(admin.ModelAdmin):
    list_display = ["id", "img", "author"]


admin.site.register(Photograph, PhotographAdmin)
