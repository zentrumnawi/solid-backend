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
    fields = [("position", "active"), "title", "title_image", "categories"]
    list_display = ["id", "title", "position", "title_image", "active"]
    list_display_links = ["title"]
    inlines = [SlideshowPageInline]
    raw_id_fields = ["title_image"]


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
    list_display = [
        "id",
        "title",
        "show_with_position",
        "page_with_position",
        "position",
        "image",
    ]
    list_display_links = ["title"]
    ordering = ["page__show__position", "page__position", "position"]

    def show_with_position(self, obj):
        # Show field that is sortable by it's position
        return "{} ({})".format(obj.page.show, obj.page.show.position)

    show_with_position.short_description = "Show (position)"
    show_with_position.admin_order_field = "page__show__position"

    def page_with_position(self, obj):
        # Page field that is sortable by it's position
        return "{} ({})".format(obj.page, obj.page.position)

    page_with_position.short_description = "Page (position)"
    page_with_position.admin_order_field = "page__position"
    raw_id_fields = ["image", "page"]


admin.site.register(SlideshowImage, SlideshowImageAdmin)
