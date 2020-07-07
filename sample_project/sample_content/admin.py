from django.contrib import admin
from .models import MyProfile
from solid_backend.photograph.admin import PhotographInline
# Register your models here.

class MyProfileAdmin(admin.ModelAdmin):
    inlines = [
        PhotographInline,
    ]


admin.site.register(MyProfile, MyProfileAdmin)
