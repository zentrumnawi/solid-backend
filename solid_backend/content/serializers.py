from importlib import import_module

from django.conf import settings
from rest_framework import serializers

from .models import TreeNode


class TreeNodeSerializer(serializers.ModelSerializer):

    profiles = getattr(
        import_module(settings.PROFILES_SERIALIZER_MODULE), settings.PROFILES_SERIALIZER
    )(many=True, required=False)
    children = serializers.SerializerMethodField()

    class Meta:
        depth = 1
        model = TreeNode
        fields = ("name", "info", "profiles", "children")

    def get_children(self, obj):
        return TreeNodeSerializer(obj.get_children(), many=True).data
