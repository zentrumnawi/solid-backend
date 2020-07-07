from django.contrib import admin

from solid_backend.photograph.admin import PhotographInline

from .models import MyProfile

# Register your models here.


class MyProfileAdmin(admin.ModelAdmin):
    inlines = [
        PhotographInline,
    ]


admin.site.register(MyProfile, MyProfileAdmin)
