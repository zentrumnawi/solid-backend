from django.contrib import admin
from .models import Message
from solid_backend.utility.forms import HasImgForm, DateOrderForm


class MessageForm(HasImgForm, DateOrderForm):
    pass


class MessageAdmin(admin.ModelAdmin):
    form = MessageForm
    list_display = ["id", "type", "title", "valid_from", "valid_to", "img"]


admin.site.register(Message, MessageAdmin)
