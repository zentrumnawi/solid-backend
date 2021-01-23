from django import forms
from django.db import models


class ConcatWidget(forms.MultiWidget):
    """
    A Widget consisting of multiple Select inputs
    depending on how many sets of choices are provided.
    """

    def __init__(self, concat_choices, seperators, attrs=None):
        self.seperators = seperators
        self.choice_cnt = len(concat_choices)
        widgets = [forms.Select(choices=choices_set) for choices_set in concat_choices]
        display_field = forms.Textarea()
        display_field.attrs["readonly"] = True
        display_field.attrs["style"] = "border: none; font-weight: bold; resize: none;"
        display_field.attrs["rows"] = 1

        widgets.append(display_field)
        super().__init__(widgets, attrs)

    def decompress(self, value):
        # raise Exception(value is "")
        seperator_cnt = len(self.seperators)
        ret_list = value.split(f"{self.seperators[0]}")
        if seperator_cnt > 1:
            # last value is concatenated by the second seperator
            last_value = ret_list.pop(-1)
            ret_list.extend(last_value.split(f"{self.seperators[1]}"))
            # raise Exception(ret_list)
        if len(ret_list) < self.choice_cnt:
            ret_list.extend(
                (self.choice_cnt - len(ret_list)) * ["",]
            )
        ret_list.append("Saved value: {}".format(value))
        return ret_list


class ConcatFormField(forms.MultiValueField):
    """
    A form field accepting multiple sets of choices
    and concatenates them.
    """

    def __init__(self, **kwargs):
        kwargs.pop("max_length")
        self.concat_choices = kwargs.pop("concat_choices", None)
        self.seperators = kwargs.pop("seperators", None)
        assert self.concat_choices
        assert self.seperators
        fields = [forms.CharField(required=False) for choice_set in self.concat_choices]
        super(ConcatFormField, self).__init__(
            fields=fields, require_all_fields=False, **kwargs
        )
        self.widget = ConcatWidget(
            concat_choices=self.concat_choices, seperators=self.seperators
        )

    def compress(self, data_list):
        """
        Join the provideded data depending on
        1. the number of selected values
        2. the number of seperators

        We have two use cases to cover here:
        For example:
        I)
        seperators = [", ", ] and
        n vlaues selected
        ---> concat just with ","
        1 value selected
        ---> just save the value
        II)
        seperators = [", ", " and "] and
        n vlaues selected
        ---> concat n-1 just with "," and join the last one with "and"
        1 value selected
        ---> just save the value

        The actual seperators aren't that important but we
        by covering the two cases the you get to choose the readability of you concatenation.
        :param data_list:
        :return:
        """
        # Filter out not provided values
        data_list = list(filter(lambda x: x != "", data_list))
        seperator_cnt = len(self.seperators)
        data_cnt = len(data_list)
        if data_cnt > 1:
            if seperator_cnt > 1:
                result = f"{self.seperators[0]}".join(data_list[:-1])
                return f"{result}{self.seperators[1]}{data_list[-1]}"
            return f"{self.seperators[0]}".join(data_list)
        elif data_cnt == 1:
            return data_list[0]
        else:
            return ""


class ConcatCharField(models.CharField):
    """
    Database Field which takes choices to be concatenated.
    """

    def __init__(self, concat_choices, seperators, *args, **kwargs):
        self.concat_choices = concat_choices
        self.seperators = seperators
        super(ConcatCharField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        # This is a fairly standard way to set up some defaults
        # while letting the caller override them.
        defaults = {
            "form_class": ConcatFormField,
            "concat_choices": self.concat_choices,
            "seperators": self.seperators,
        }
        defaults.update(kwargs)
        return super().formfield(**defaults)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs["concat_choices"] = self.concat_choices
        kwargs["seperators"] = self.seperators
        return name, path, args, kwargs


# TODO: There has to be a more elegent way of defining this Field than to "copy&paste" it.
class FromToConcatField(models.CharField):
    def __init__(self, from_choices, to_choices, *args, **kwargs):
        self.concat_choices = [from_choices, to_choices]
        self.seperators = [
            " bis ",
        ]
        super(FromToConcatField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        # This is a fairly standard way to set up some defaults
        # while letting the caller override them.
        defaults = {
            "form_class": ConcatFormField,
            "concat_choices": self.concat_choices,
            "seperators": self.seperators,
        }
        defaults.update(kwargs)
        return super().formfield(**defaults)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs["from_choices"] = self.concat_choices[0]
        kwargs["to_choices"] = self.concat_choices[1]
        return name, path, args, kwargs
