from rest_framework import serializers

from solid_backend.photograph.serializers import PhotographSerializer

from .models import Message


class MessageSerializer(serializers.ModelSerializer):
    img = PhotographSerializer(required=False)

    class Meta:
        model = Message
        fields = "__all__"
