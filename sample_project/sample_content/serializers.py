from rest_framework import serializers

from solid_backend.media_object.serializers import MediaObjectSerializer
from solid_backend.utils.serializers import SolidModelSerializer


from .models import SampleProfile, SecondSampleProfile


class SampleProfileSerializer(SolidModelSerializer):
    media_objects = MediaObjectSerializer(many=True)

    class Meta:
        model = SampleProfile
        fields = "__all__"
        depth = 1


class SecondSampleProfileSerializer(SolidModelSerializer):
    media_objects = MediaObjectSerializer(many=True)

    class Meta:
        model = SecondSampleProfile
        fields = "__all__"
        depth = 1
