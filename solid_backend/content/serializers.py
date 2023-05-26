from importlib import import_module

from django.conf import settings
from rest_framework import serializers

from solid_backend.utils.serializers import RecursiveSerializer

from .models import TreeNode

SERIALIZERS = {}

if hasattr(settings, "PROFILES_SERIALIZERS"):
    for field_name in settings.PROFILES_SERIALIZERS:
        module, serializer = settings.PROFILES_SERIALIZERS[field_name]
        SERIALIZERS[field_name] = getattr(import_module(module), serializer)


class IdTreeNodeSerializer(serializers.ModelSerializer):
    def build_nested_field(self, field_name, relation_info, nested_depth):
        if SERIALIZERS.get(field_name) is not None:
            return SERIALIZERS.get(field_name), {"many": True, "required": False}

        return self.build_relational_field(
            field_name, relation_info
        )

    class Meta:
        model = TreeNode
        fields = ("name", "info", "children", "level") + tuple(
            settings.PROFILES_SERIALIZERS.keys()
        )
        depth = 1


class NestedTreeNodeSerializer(IdTreeNodeSerializer):
    def build_nested_field(self, field_name, relation_info, nested_depth):
        if SERIALIZERS.get(field_name) is not None:
            return SERIALIZERS.get(field_name), {"many": True, "required": False}

        return super(NestedTreeNodeSerializer, self).build_nested_field(
            field_name, relation_info, nested_depth
        )

    children = RecursiveSerializer(many=True, required=False)

    class Meta:
        model = TreeNode
        fields = ("name", "info", "children", "level") + tuple(
            settings.PROFILES_SERIALIZERS.keys()
        )
        depth = 2
