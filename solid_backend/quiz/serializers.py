from rest_framework import serializers

from solid_backend.photograph.serializers import PhotographSerializer
from solid_backend.utils.serializers import DynamicExcludeModelSerializer

from .models import QuizAnswer, QuizQuestion


class QuizAnswerSerializer(DynamicExcludeModelSerializer):
    class Meta:
        model = QuizAnswer
        fields = "__all__"


class QuizQuestionSerializer(serializers.ModelSerializer):
    answers = QuizAnswerSerializer(exclude="question", many=True, required=False)
    img = PhotographSerializer(many=True, required=False)

    class Meta:
        model = QuizQuestion
        fields = "__all__"
