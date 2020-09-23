from rest_framework import serializers

from solid_backend.photograph.serializers import PhotographSerializer

from .models import QuizAnswer, QuizQuestion


class QuizQuestionLessSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizQuestion
        fields = "__all__"


class QuizAnswerLessSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizAnswer
        fields = "__all__"


class QuizQuestionSerializer(serializers.ModelSerializer):
    answers = QuizAnswerLessSerializer(many=True)
    img = PhotographSerializer(many=True)

    class Meta:
        model = QuizQuestion
        fields = "__all__"


class QuizAnswerSerializer(serializers.ModelSerializer):
    question = QuizQuestionLessSerializer()

    class Meta:
        model = QuizAnswer
        fields = "__all__"
