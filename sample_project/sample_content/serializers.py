from rest_framework import serializers

from solid_backend.photograph.serializers import PhotographSerializer

from .models import SampleProfile


class SampleProfileSerializer(serializers.ModelSerializer):
    photographs = PhotographSerializer(many=True)

    class Meta:
        model = SampleProfile
        fields = "__all__"
        depth = 1
