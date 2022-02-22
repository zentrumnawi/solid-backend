from django import forms
from django.contrib.contenttypes.forms import BaseGenericInlineFormSet
from django.core.validators import FileExtensionValidator
from django.utils.translation import ugettext_lazy as _

REQUIRED_ANSWER_FIELDS = {
    "SC": ["text", "correct", "feedback_correct", "feedback_incorrect"],
    "MC": ["text", "correct", "feedback_correct", "feedback_incorrect"],
    "TF": ["text", "correct", "feedback_correct", "feedback_incorrect"],
    "RN": ["text", "feedback_correct", "feedback_incorrect", "ranking_position", "subsequences",
           "feedback_subsequences"],
    "RG": ["range_value", "range_max", "range_min", "range_step", "tolerance", "feedback_correct",
           "feedback_incorrect", ],
}


class QuizAnswerForm(forms.ModelForm):

    def clean(self):
        question_type = self.data["type"]
        self.validate_required_fields(q_type=question_type)
        self.check_unnecessary_data(q_type=question_type)
        cleaned_data = super(QuizAnswerForm, self).clean()
        return cleaned_data

    def validate_required_fields(self, q_type):
        """
        All fields are per definition not required.
        This state changes depending on the type of Question an answer belongs to.
        :param q_type:
        :return:
        """
        for field in REQUIRED_ANSWER_FIELDS[q_type]:
            self.fields[field].required = True
        super(QuizAnswerForm, self)._clean_fields()

    def check_unnecessary_data(self, q_type):
        """
        Check wether data was provided for fields which are not
        necessary for the given question type.
        :param q_type:
        :return:
        """
        errors= []
        fields_to_check = REQUIRED_ANSWER_FIELDS[q_type] + ["question", "DELETE", "id"]
        for field in self.fields:
            if field not in fields_to_check and self.cleaned_data[field] is not None:
                self.add_error(
                    "__all__",
                    "You can not provide a value for the field {} since this field"
                    " is not required for this Question type.".format(field)
                )
