from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import QuizAnswer, QuizQuestion
from .serializers import QuizAnswerSerializer, QuizQuestionSerializer


class QuizQuestionEndpoint(ReadOnlyModelViewSet):
    """
    Endpoint that provides the database table of all quiz questions including their answers.
    """

    queryset = QuizQuestion.objects.all()
    serializer_class = QuizQuestionSerializer
    name = "quizquestion"


class QuizAnswerEndpoint(ReadOnlyModelViewSet):
    """
    Endpoint that provides the database table of all quiz answers.
    """

    queryset = QuizAnswer.objects.all()
    serializer_class = QuizAnswerSerializer
    name = "quizanswer"
