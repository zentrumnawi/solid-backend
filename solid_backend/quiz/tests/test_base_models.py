from django.contrib.postgres.fields import ArrayField
from django.db import models
from taggit.managers import TaggableManager
from django.contrib.contenttypes.fields import GenericRelation


class TestQuizQuestionModelExists:
    def test_model_exists(self):
        """
        Test whether an object QuizQuestion can be imported.
        """

    def test_model_is_django_model(self):
        """
        Test if the QuizQuestion object is a Django model.
        """

        from solid_backend.quiz.models import QuizQuestion

        assert issubclass(QuizQuestion, models.Model)


class TestQuizAnswerModelExists:
    def test_model_exists(self):
        """
        Test whether an object QuizAnswer can be imported.
        """

    def test_model_is_django_model(self):
        """
        Test if the QuizAnswer object is a Django model.
        """

        from solid_backend.quiz.models import QuizAnswer

        assert issubclass(QuizAnswer, models.Model)


class TestQuizQuestionModelFields:
    """
    Test suite with basic field tests whether all fields of the QuizQuestion object
    exist and have the correct class instance and field attribute values.
    """

    def test_model_has_field_type(self, quiz_question_model_class):
        assert hasattr(quiz_question_model_class, "type")

    def test_model_has_field_difficulty(self, quiz_question_model_class):
        assert hasattr(quiz_question_model_class, "difficulty")

    def test_model_has_field_text(self, quiz_question_model_class):
        assert hasattr(quiz_question_model_class, "text")

    def test_model_has_field_img(self, quiz_question_model_class):
        assert hasattr(quiz_question_model_class, "img")

    def test_model_has_field_tags(self, quiz_question_model_class):
        assert hasattr(quiz_question_model_class, "tags")

    def test_field_type_type(self, quiz_question_model_class):
        assert isinstance(
            quiz_question_model_class._meta.get_field("type"), models.CharField
        )

    def test_field_type_difficulty(self, quiz_question_model_class):
        assert isinstance(
            quiz_question_model_class._meta.get_field("difficulty"),
            models.PositiveSmallIntegerField,
        )

    def test_field_type_text(self, quiz_question_model_class):
        assert isinstance(
            quiz_question_model_class._meta.get_field("text"), models.TextField
        )

    def test_field_type_img(self, quiz_question_model_class):
        assert isinstance(
            quiz_question_model_class._meta.get_field("img"), GenericRelation
        )

    def test_field_type_tags(self, quiz_question_model_class):
        assert isinstance(quiz_question_model_class._meta.get_field("tags"), TaggableManager)

    def test_field_attribute_values_img(
        self, quiz_question_model_class, media_object_model_class
    ):
        field = quiz_question_model_class._meta.get_field("img")
        assert issubclass(field.related_model, media_object_model_class)


class TestQuizAnswerModelFields:
    """
    Test suite with basic field tests whether all fields of the QuizAnswer object exist
    and have the correct class instance.
    """

    def test_model_has_field_question(self, quiz_answer_model_class):
        assert hasattr(quiz_answer_model_class, "question")

    def test_model_has_field_text(self, quiz_answer_model_class):
        assert hasattr(quiz_answer_model_class, "text")

    def test_model_has_field_correct(self, quiz_answer_model_class):
        assert hasattr(quiz_answer_model_class, "correct")

    def test_model_has_field_feedback_correct(self, quiz_answer_model_class):
        assert hasattr(quiz_answer_model_class, "feedback_correct")

    def test_model_has_field_feedback_incorrect(self, quiz_answer_model_class):
        assert hasattr(quiz_answer_model_class, "feedback_incorrect")

    def test_field_type_question(self, quiz_answer_model_class):
        assert isinstance(
            quiz_answer_model_class._meta.get_field("question"), models.ForeignKey
        )

    def test_field_type_text(self, quiz_answer_model_class):
        assert isinstance(
            quiz_answer_model_class._meta.get_field("text"), models.CharField
        )

    def test_field_type_correct(self, quiz_answer_model_class):
        assert isinstance(
            quiz_answer_model_class._meta.get_field("correct"), models.BooleanField
        )

    def test_field_type_feedback_correct(self, quiz_answer_model_class):
        assert isinstance(
            quiz_answer_model_class._meta.get_field("feedback_correct"),
            models.CharField,
        )

    def test_field_type_feedback_incorrect(self, quiz_answer_model_class):
        assert isinstance(
            quiz_answer_model_class._meta.get_field("feedback_incorrect"),
            models.CharField,
        )
