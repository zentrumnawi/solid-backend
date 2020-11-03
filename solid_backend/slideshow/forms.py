from django import forms

from .models import Slideshow, SlideshowImage, SlideshowPage


class SlideshowInlineAdminFormSet(forms.BaseInlineFormSet):
    """
    Validate if position is available and order froms by position.
    """

    def clean(self):
        super().clean()

        positions = []

        for form in self.forms:
            if form.cleaned_data.get("DELETE"):
                continue
            position = form.cleaned_data.get("position")
            positions.append(position)

            if positions.count(position) > 1:
                form.add_error("position", "This position is not available.")

    def get_queryset(self):
        return super().get_queryset().order_by("position")


class SlideshowAdminForm(forms.ModelForm):
    """
    Validate if position is available.
    """

    def clean(self):
        super().clean()

        position_field = self.fields.get("position")
        initial_position = self.get_initial_for_field(position_field, "position")
        position = self.cleaned_data.get("position")
        model = type(self.instance)

        if model == Slideshow:
            objects = model.objects.all()
        elif model == SlideshowPage:
            objects = model.objects.filter(show=self.cleaned_data.get("show"))
        elif model == SlideshowImage:
            objects = model.objects.filter(page=self.cleaned_data.get("page"))
        else:
            raise TypeError("Only Slideshow, SlideshowPage, SlideshowImage allowed.")

        if position_field.has_changed(initial_position, position):
            for obj in objects:
                if position == obj.position:
                    self.add_error("position", "This position is not available.")
