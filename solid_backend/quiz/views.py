from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.views import Response
from rest_framework.generics import ListAPIView
from taggit.models import TaggedItem
from taggit.serializers import TagListSerializerField

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


class QuizMetaDataEndpoint(ListAPIView):

    def list(self, request, *args, **kwargs):
        tags_used = TaggedItem.tags_for(QuizQuestion)
        difficulties_used =list(
            map(
                lambda x: x["difficulty"],
                QuizQuestion.objects.all().values("difficulty").distinct()
            )
        )
        question_count = QuizQuestion.objects.count()
        data = {
            "tags": TagListSerializerField().to_representation(tags_used),
            "difficulties": difficulties_used,
            "question_count": question_count
        }
        return Response(data=data)
