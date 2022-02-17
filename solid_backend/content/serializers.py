from importlib import import_module

from django.conf import settings
from rest_framework import serializers

from solid_backend.utils.serializers import RecursiveSerializer

from .models import TreeNode

SERIALIZERS = []

if hasattr(settings, "PROFILES_SERIALIZERS"):
    for field_name in settings.PROFILES_SERIALIZERS:
        SERIALIZERS.append(
            (
                field_name, getattr(
                    import_module(settings.PROFILES_SERIALIZER_MODULE),
                    settings.PROFILES_SERIALIZER_NAME,
                )(many=True, required=False)
            )
        )


class TreeNodeSerializer(serializers.ModelSerializer):
    # To use a custom serializer for the profiles field, it must be specified in the
    # settings with PROFILES_SERIALIZER_MODULE and PROFILES_SERIALIZER_NAME.
    def __init__(self, *args, **kwargs):
        super(TreeNodeSerializer, self).__init__(*args, **kwargs)
        for field, serializer in SERIALIZERS:
            setattr(self, field, serializer)

    children = RecursiveSerializer(many=True, required=False)

    class Meta:
        model = TreeNode
        fields = ("name", "info", "children") + tuple(settings.PROFILES_SERIALIZERS.keys())
        depth = 2
