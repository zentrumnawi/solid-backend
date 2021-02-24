from django.contrib import admin, messages
from django.contrib.contenttypes.admin import GenericTabularInline

from .forms import PhotographAdminForm, PhotographInlineFormSet
from .models import Photograph

fields = [
    "profile_position",
    ("img", "dzi_option"),
    "img_alt",
    "description",
    "dzi_file",
    "img_original_width",
    "img_original_height",
    ("length_value", "length_unit", "pixel_number"),
    "img_original_scale",
    "audio",
    "audio_duration",
    "date",
    "author",
    "license",
]
readonly_fields = [
    "dzi_file",
    "img_original_width",
    "img_original_height",
    "img_original_scale",
    "audio_duration",
]


class DeepZoomAdmin(admin.ModelAdmin):
    actions = ["switch_dzi_option"]

    def delete_queryset(self, request, queryset):
        # Call DeepZoom model delete method for each selected object during bulk delete
        # via admin action to ensure that the Deep Zoom directory trees will be deleted.
        for obj in queryset:
            obj.delete()

    def switch_dzi_option(self, request, queryset):
        # Switch the Deep Zoom option for each selected object and either create or
        # delete its Deep Zoom image files.
        for obj in queryset:
            if not obj.dzi_option:
                obj.dzi_option = True
            else:
                obj.dzi_option = False
            obj.save()

        n = queryset.count()

        self.message_user(
            request,
            "Successfully switched Deep Zoom option on {} {}.".format(
                n, admin.utils.model_ngettext(self.opts, n)
            ),
            messages.SUCCESS,
        )

    switch_dzi_option.short_description = (
        "Switch Deep Zoom option on selected photographs"
    )


class PhotographInline(GenericTabularInline):
    model = Photograph
    form = PhotographAdminForm
    formset = PhotographInlineFormSet
    extra = 1
    fields = fields
    readonly_fields = readonly_fields


class PhotographAdmin(DeepZoomAdmin):
    form = PhotographAdminForm
    fields = ["profile"] + fields
    readonly_fields = ["profile", "profile_position"] + readonly_fields
    list_display = ["id", "profile", "img", "dzi_option", "author", "license"]

    def profile(self, obj):
        if not obj.profile:
            return "-"
        return str(obj.profile)


admin.site.register(Photograph, PhotographAdmin)
