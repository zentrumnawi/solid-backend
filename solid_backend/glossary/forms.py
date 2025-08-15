from django import forms
from django.forms import ModelForm, ValidationError
from django.utils.translation import ugettext_lazy as _
from .models import GlossaryEntry
from django.conf import settings

class GlossaryEntryAdminForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.should_show_tags():
            self.fields['tags'] = forms.ChoiceField(
                choices=settings.GLOSSARY_TABS,
                widget=forms.Select,
                required=False,
                help_text="Select applicable tags"
            )
        else:
            self.exclude = ('tags')

    def should_show_tags(self):
        return hasattr(settings, 'GLOSSARY_TABS')

    def clean(self):
        data = super(GlossaryEntryAdminForm, self).clean()

        if not (data.get("text", None) or data.get("links", None)):
            raise ValidationError(
                _(
                    "Es muss entweder ein Text oder eine Verknüpfung zu einem anderen Eintrag angegeben werden."
                )
            )
        return data