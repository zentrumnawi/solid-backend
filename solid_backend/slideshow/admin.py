from django.contrib import admin

from .forms import SlideshowAdminForm, SlideshowInlineAdminFormSet
from .models import Slideshow, SlideshowImage, SlideshowPage


class SlideshowPageInline(admin.TabularInline):
    model = SlideshowPage
    formset = SlideshowInlineAdminFormSet
    extra = 1


class SlideshowImageInline(admin.TabularInline):
    model = SlideshowImage
    formset = SlideshowInlineAdminFormSet
    extra = 1


class SlideshowAdmin(admin.ModelAdmin):
    form = SlideshowAdminForm
    fields = [("position", "active"), "title", "img"]
    list_display = ["id", "title", "position", "img", "active"]
    list_display_links = ["title"]
    inlines = [SlideshowPageInline]


admin.site.register(Slideshow, SlideshowAdmin)


class SlideshowPageAdmin(admin.ModelAdmin):
    form = SlideshowAdminForm
    list_display = ["id", "title", "position", "show"]
    list_display_links = ["title"]
    inlines = [SlideshowImageInline]


admin.site.register(SlideshowPage, SlideshowPageAdmin)


class SlideshowImageAdmin(admin.ModelAdmin):
    form = SlideshowAdminForm
    list_display = ["id", "title", "position", "show_page", "img"]
    list_display_links = ["title"]

    def show_page(self, obj):
        return "{} : {}".format(
            getattr(SlideshowPage.objects.get(id=obj.page.id), "show"), obj.page
        )

    show_page.short_description = "Show : Page"


admin.site.register(SlideshowImage, SlideshowImageAdmin)
