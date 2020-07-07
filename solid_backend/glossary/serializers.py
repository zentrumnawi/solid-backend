from rest_framework import serializers

from .models import GlossaryEntry


class GlossaryEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = GlossaryEntry
        fields = "__all__"
