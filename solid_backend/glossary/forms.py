from django import forms
from django.forms import ModelForm, ValidationError
from django.utils.translation import ugettext_lazy as _
from .models import GlossaryEntry
from django.conf import settings


class GlossaryEntryAdminForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.should_show_tags():
            self.fields["tags"].widget = forms.Select(choices=settings.GLOSSARY_TABS)
            self.fields["tags"].help_text = "Select applicable tags"

    def should_show_tags(self):
        return hasattr(settings, "GLOSSARY_TABS")

    def clean(self):

        data = super().clean()

        if not (data.get("text", None) or data.get("links", None)):
            raise ValidationError(
                _(
                    "Es muss entweder ein Text oder eine Verknüpfung zu einem anderen Eintrag angegeben werden."
                )
            )

        # Handle regular fields
        for field_name, value in self.data.items():
            if field_name in self.fields and field_name != "links":  # exclude M2M
                data[field_name] = value

        # Handle M2M field separately
        if "links" in self.data:
            # necessary to save multiple links
            links_data = self.data.getlist("links")
            data["links"] = links_data

        return data
