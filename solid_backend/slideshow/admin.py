from django.contrib import admin

from .forms import SlideshowAdminForm, SlideshowInlineFormSet
from .models import Slideshow, SlideshowImage, SlideshowPage


class SlideshowPageInline(admin.TabularInline):
    model = SlideshowPage
    formset = SlideshowInlineFormSet
    extra = 1


class SlideshowImageInline(admin.TabularInline):
    model = SlideshowImage
    formset = SlideshowInlineFormSet
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
    list_display = ["id", "title", "show_with_position", "position"]
    list_display_links = ["title"]
    inlines = [SlideshowImageInline]
    ordering = ["show__position", "position"]

    def show_with_position(self, obj):
        # Show field that is sortable by it's position
        return "{} ({})".format(obj.show, obj.show.position)

    show_with_position.short_description = "Show (position)"
    show_with_position.admin_order_field = "show__position"


admin.site.register(SlideshowPage, SlideshowPageAdmin)


class SlideshowImageAdmin(admin.ModelAdmin):
    form = SlideshowAdminForm
    list_display = ["id", "title", "show_page", "position", "img"]
    list_display_links = ["title"]
    ordering = ["page__show__position", "page__position", "position"]

    def show_page(self, obj):
        return "{} : {}".format(
            getattr(SlideshowPage.objects.get(id=obj.page.id), "show"), obj.page
        )

    show_page.short_description = "Show : Page"


admin.site.register(SlideshowImage, SlideshowImageAdmin)
