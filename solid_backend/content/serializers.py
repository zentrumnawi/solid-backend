from importlib import import_module

from django.conf import settings
from rest_framework import serializers

from solid_backend.utils.serializers import RecursiveSerializer

from .models import TreeNode

PROFILES_SERIALIZER = None

if hasattr(settings, "PROFILES_SERIALIZER_MODULE"):
    PROFILES_SERIALIZER = getattr(
        import_module(settings.PROFILES_SERIALIZER_MODULE),
        settings.PROFILES_SERIALIZER_NAME,
    )(many=True, required=False)


class TreeNodeSerializer(serializers.ModelSerializer):
    # To use a custom serializer for the profiles field, it must be specified in the
    # settings with PROFILES_SERIALIZER_MODULE and PROFILES_SERIALIZER_NAME.
    if PROFILES_SERIALIZER:
        profiles = PROFILES_SERIALIZER

    children = RecursiveSerializer(many=True, required=False)

    class Meta:
        model = TreeNode
        fields = ("name", "info", "profiles", "children")
        depth = 2
