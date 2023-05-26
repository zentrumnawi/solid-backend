from rest_framework import serializers

from solid_backend.media_object.serializers import MediaObjectSerializer
from solid_backend.photograph.serializers import PhotographSerializer

from .models import SampleProfile, SecondSampleProfile


class SampleProfileSerializer(serializers.ModelSerializer):
    media_objects = MediaObjectSerializer(many=True)

    class Meta:
        model = SampleProfile
        fields = "__all__"


class SecondSampleProfileSerializer(serializers.ModelSerializer):
    media_objects = MediaObjectSerializer(many=True)

    class Meta:
        model = SecondSampleProfile
        fields = "__all__"
        depth = 1
