from django.db.models import Case, When
from rest_framework import serializers
from random import sample

from solid_backend.photograph.serializers import PhotographSerializer
from solid_backend.utils.serializers import DynamicExcludeModelSerializer

from .models import QuizAnswer, QuizQuestion


class RandomListSerializer(serializers.ListSerializer):
    """
    A ListSerializer which if used as a child serializer shuffles the data once and returns them.
    IF one shuffle actually returns the original Order we inverse the order and return it.
    """

    def to_representation(self, data):

        if self.parent is None:
            return super(RandomListSerializer, self).to_representation(data)

        # Fall back to shuffling the ids to compare whether the shuffling returned the original order
        orig_id_list = list(data.values_list("pk", flat=True))
        shuffled_ids = sample(orig_id_list, len(orig_id_list))
        if shuffled_ids == orig_id_list:
            shuffled_ids = reversed(shuffled_ids)
        preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(shuffled_ids)])
        return super(RandomListSerializer, self).to_representation(data.order_by(preserved))


class QuizAnswerSerializer(DynamicExcludeModelSerializer):

    class Meta:
        model = QuizAnswer
        fields = "__all__"
        list_serializer_class = RandomListSerializer


class QuizQuestionSerializer(serializers.ModelSerializer):
    answers = QuizAnswerSerializer(many=True, required=False)
    img = PhotographSerializer(many=True, required=False)

    class Meta:
        model = QuizQuestion
        fields = "__all__"
