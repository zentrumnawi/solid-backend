from django import forms


class HasImgForm(forms.ModelForm):
    """
    Validate if an image and an alternate text for the image are provided together.
    """

    def clean(self):
        img = self.cleaned_data.get("img")
        img_alt = self.cleaned_data.get("img_alt")

        if img and not img_alt:
            error_message = "Provide an alternate text for the image."
            self.add_error("img_alt", error_message)

        if img_alt and not img:
            error_message = (
                'Please select an image for upload or leave the "img alt" field empty.'
            )
            self.add_error("img_alt", error_message)

        super(HasImgForm, self).clean()
