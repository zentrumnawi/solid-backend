from django import forms
from django.contrib import admin

from .models import Message


class DateOrderForm(forms.ModelForm):
    """
    Validate whether a validity start date and end date are in the correct order.
    """

    def clean(self):
        valid_from = self.cleaned_data.get("valid_from")
        valid_to = self.cleaned_data.get("valid_to")

        if valid_to is not None and valid_to < valid_from:
            error_message = "Ensure the end date is equal with or after the start date."
            self.add_error("valid_to", error_message)

        super(DateOrderForm, self).clean()


class MessageAdmin(admin.ModelAdmin):
    form = DateOrderForm
    list_display = ["id", "type", "title", "valid_from", "valid_to", "img"]


admin.site.register(Message, MessageAdmin)
