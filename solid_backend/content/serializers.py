from importlib import import_module

from django.conf import settings
from rest_framework import serializers

from .models import TreeNode


class TreeNodeSerializer(serializers.ModelSerializer):
    # To use a custom serializer for the profiles field, it must be specified in the
    # settings with PROFILES_SERIALIZER_MODULE and PROFILES_SERIALIZER.
    if hasattr(settings, "PROFILES_SERIALIZER_MODULE"):
        profiles = getattr(
            import_module(settings.PROFILES_SERIALIZER_MODULE),
            settings.PROFILES_SERIALIZER,
        )(many=True)

    children = serializers.SerializerMethodField()

    class Meta:
        model = TreeNode
        fields = ("name", "info", "profiles", "children")
        depth = 2

    def get_children(self, obj):
        return TreeNodeSerializer(obj.get_children(), many=True).data
