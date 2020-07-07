import pytest

from solid_backend.quiz.models import QuizAnswer, QuizQuestion


@pytest.fixture
def quiz_question_model_class():
    return QuizQuestion


@pytest.fixture
def quiz_answer_model_class():
    return QuizAnswer
