from django import forms


class HasImgForm(forms.ModelForm):
    """
    Validate if an image and an alternate text for the image are provided together.
    """

    def clean(self):
        img = self.cleaned_data.get("img")
        img_alt = self.cleaned_data.get("img_alt")

        if img and not img_alt:
            error_message = "An alternate text for the image needs to be provided."
            self.add_error("img_alt", error_message)

        if img_alt and not img:
            error_message = (
                'Please select an image for upload or leave the "img alt" field empty.'
            )
            self.add_error("img_alt", error_message)

        super(HasImgForm, self).clean()


class DateOrderForm(forms.ModelForm):
    """
    Validate whether a validity start date and end date are in the correct order.
    """

    def clean(self):
        valid_from = self.cleaned_data.get("valid_from")
        valid_to = self.cleaned_data.get("valid_to")

        if valid_to is not None and valid_to < valid_from:
            error_message = (
                "The validity end date must be equel with or after the start date."
            )
            self.add_error("valid_to", error_message)

        super(DateOrderForm, self).clean()
