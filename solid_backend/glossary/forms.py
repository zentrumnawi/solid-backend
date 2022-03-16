from django.forms import ModelForm, ValidationError
from django.utils.translation import ugettext_lazy as _


class GlossaryEntryAdminForm(ModelForm):
    def clean(self):
        data = super(GlossaryEntryAdminForm, self).clean()

        if not (data.get("text", None) or data.get("links", None)):
            raise ValidationError(
                _(
                    "Es muss entweder ein Text oder eine Verknüpfung zu einem anderen Eintrag angegeben werden."
                )
            )
        return data
