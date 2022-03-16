from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.views import Response
from rest_framework.generics import ListAPIView
from taggit.models import TaggedItem
from taggit.serializers import TagListSerializerField
from taggit.forms import TagField
from django_filters import rest_framework as filters
from random import sample

from .models import QuizAnswer, QuizQuestion
from .serializers import QuizAnswerSerializer, QuizQuestionSerializer


class TagsFilter(filters.CharFilter):
    field_class = TagField

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("lookup_expr", "in")
        super(TagsFilter, self).__init__(*args, **kwargs)


class IntegerInFilter(filters.BaseInFilter, filters.NumberFilter):
    pass


class QuizSessionFilter(filters.FilterSet):

    tags = TagsFilter(field_name="tags__name", distinct=True)
    difficulty = IntegerInFilter("difficulty")

    class Meta:
        model = QuizQuestion
        fields = ["tags", "difficulty"]


class QuizSessionEndpoint(ListAPIView):

    queryset = QuizQuestion.objects.all()
    serializer_class = QuizQuestionSerializer
    name = "quizsession"
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = QuizSessionFilter

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        question_count = int(request.GET["count"])
        if question_count < queryset.count():
            queryset = sample(list(queryset), k=question_count)
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)


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
        difficulties_used = list(
            map(
                lambda x: x["difficulty"],
                QuizQuestion.objects.all().values("difficulty").distinct(),
            )
        )
        question_count = QuizQuestion.objects.count()
        data = {
            "tags": TagListSerializerField().to_representation(tags_used),
            "difficulties": difficulties_used,
            "question_count": question_count,
        }
        return Response(data=data)
