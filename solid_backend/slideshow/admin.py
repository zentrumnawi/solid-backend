from django.contrib import admin

from .models import Slideshow, SlideshowImage, SlideshowPage


class SlideshowPageInline(admin.TabularInline):
    model = SlideshowPage
    extra = 1


class SlideshowImageInline(admin.TabularInline):
    model = SlideshowImage
    extra = 1


class SlideshowAdmin(admin.ModelAdmin):
    fields = [("position", "active"), "title", "img"]
    list_display = ["id", "title", "position", "img", "active"]
    list_display_links = ["title"]
    inlines = [SlideshowPageInline]


admin.site.register(Slideshow, SlideshowAdmin)


class SlideshowPageAdmin(admin.ModelAdmin):
    list_display = ["id", "show", "position", "title"]
    inlines = [SlideshowImageInline]


admin.site.register(SlideshowPage, SlideshowPageAdmin)


class SlideshowImageAdmin(admin.ModelAdmin):
    list_display = ["id", "page", "position", "title", "img"]


admin.site.register(SlideshowImage, SlideshowImageAdmin)
