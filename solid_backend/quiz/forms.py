from functools import reduce

from django.forms.models import BaseInlineFormSet, ValidationError

REQUIRED_ANSWER_FIELDS = {
    "SC": ["text", "correct", "feedback_correct", "feedback_incorrect"],
    "MC": ["text", "correct", "feedback_correct", "feedback_incorrect"],
    "TF": ["text", "correct", "feedback_correct", "feedback_incorrect"],
    "RG": [
        "text",
        "feedback_correct",
        "feedback_incorrect",
        "ranking_position",
        "subsequences",
        "feedback_subsequences",
    ],
    "RN": [
        "range_value",
        "range_max",
        "range_min",
        "range_step",
        "tolerance",
        "feedback_correct",
        "feedback_incorrect",
    ],
}


class QuizAnswerFormSet(BaseInlineFormSet):
    def clean(self):
        question_type = self.data["type"]
        for form in self.forms:
            self.validate_required_fields(form=form, q_type=question_type)
            self.check_unnecessary_data(form=form, q_type=question_type)
        assert hasattr(self, "validate_q_type_{}".format(question_type))
        forms = self.exclude_empty_forms(self.forms)
        getattr(self, "validate_q_type_{}".format(question_type))(forms)

        cleaned_data = super(QuizAnswerFormSet, self).clean()
        return cleaned_data

    def validate_required_fields(self, q_type, form):
        """
        All fields are per definition not required.
        This state changes depending on the type of Question an answer belongs to.
        :param q_type:
        :return:
        """
        for field in REQUIRED_ANSWER_FIELDS[q_type]:
            form[field].required = True
        form._clean_fields()

    def check_unnecessary_data(self, q_type, form):
        """
        Check wether data was provided for fields which are not
        necessary for the given question type.
        :param q_type:
        :return:
        """
        fields_to_check = REQUIRED_ANSWER_FIELDS[q_type] + ["question", "DELETE", "id"]
        for field in form.fields:
            if field not in fields_to_check and form.cleaned_data[field] is not None:
                form.add_error(
                    "__all__",
                    "You can not provide a value for the field {} since this field"
                    " is not required for this Question type.".format(field),
                )

    def validate_q_type_SC(self, forms):
        """
        Validate forms for question type SC - Single Choice.
        Validation:
        Only one answer may be marked as correct.
        :param forms:
        :return:
        """
        correct_cnt = reduce(
            lambda a, b: a + b, map(lambda x: x.cleaned_data["correct"], forms)
        )

        if correct_cnt != 1:
            raise ValidationError(
                "Only one answer may be correct for a Question of type Single Choice."
            )

    def validate_q_type_MC(self, forms):
        """
        Validate forms for question type MC - Multiple Choice.
        Validation:
        At least one answer must be marked as correct.
        :param forms:
        :return:
        """
        if len(forms) == 1:
            # TODO: This is not checked on DELETE
            raise ValidationError("At least two answers must be given.")

        correct_cnt = reduce(
            lambda a, b: a + b, map(lambda x: x.cleaned_data["correct"], forms)
        )

        if correct_cnt == 0:
            raise ValidationError("At least one answer must be correct.")

    def validate_q_type_TF(self, forms):
        """
        Validate forms for question type TF - True/False.
        Validation:
        Only one answer may be given.
        :param forms:
        :return:
        """

        if len(forms) != 1:
            raise ValidationError(
                "The statement of the question is either true or false. Please only provide one answer."
            )

    def validate_q_type_RG(self, forms):
        """
        Validate forms for question type Ranking - Ranking.
        Validation:
        At least two answer must be given.
        No position may exist twice.
        :param forms:
        :return:
        """
        if len(forms) < 2:
            raise ValidationError("At least two answers must be given.")

        positions = map(lambda x: x.cleaned_data["ranking_position"], forms)

        if len(forms) != len(set(positions)):
            raise ValidationError(
                "Each ranking position may only exist once. Please check your input."
            )

    def validate_q_type_RN(self, forms):
        """
        Validate forms for question type RN - Range.
        Validation:
        Only one answer may be given.
        Check for
        range_minimum < number < range_maximum
        tolerance < range_maximum - range_minimum

        :param forms:
        :return:
        """
        if len(forms) != 1:
            raise ValidationError("Please only provide one answer.")

        form = forms[0]

        if (
            not form.cleaned_data["range_max"]
            > form.cleaned_data["range_value"]
            > form.cleaned_data["range_min"]
        ):
            raise ValidationError(
                "The upper bound needs to be >= range value >= the lower bound."
            )

        if form.cleaned_data["tolerance"] >= abs(
            form.cleaned_data["range_max"] - form.cleaned_data["range_min"]
        ):
            raise ValidationError(
                "The error tolerance needs to be smaller than the given range."
            )

        if form.cleaned_data["range_step"] <= 0:
            raise ValidationError("The stepsize needs to be greater than zero.")

    def exclude_empty_forms(self, forms):
        """
        Empty forms are ignored by the normal django logic but
        we need to exclude it by hand for further validation.

        TODO:There needs to be a better way to achieve this.
        :param forms:
        :return:
        """
        return [
            form
            for form in forms
            if not (form.changed_data == [] and form.initial == {})
        ]

    def check_min_correct_answer(self, forms, n_correct=1):
        pass
