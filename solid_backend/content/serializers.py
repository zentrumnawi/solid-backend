from importlib import import_module
import logging

from django.conf import settings
from rest_framework import serializers

from solid_backend.utils.serializers import RecursiveSerializer

from .models import TreeNode

logger = logging.getLogger(__name__)

SERIALIZERS = {}

if hasattr(settings, "PROFILES_SERIALIZERS"):
    for field_name in settings.PROFILES_SERIALIZERS:
        module, serializer = settings.PROFILES_SERIALIZERS[field_name]
        SERIALIZERS[field_name] = getattr(import_module(module), serializer)


class BaseTreeNodeSerializer(serializers.ModelSerializer):
    """For getting basic node information"""

    has_children = serializers.SerializerMethodField()

    def get_has_children(self, obj):
        return obj.get_children().exists()

    class Meta:
        model = TreeNode
        fields = ("id", "name", "info", "has_children")


class TreeNodeDetailSerializer(BaseTreeNodeSerializer):
    """For detailed view of a single node, including children recursively"""

    children = RecursiveSerializer(many=True, required=False)

    class Meta(BaseTreeNodeSerializer.Meta):
        fields = BaseTreeNodeSerializer.Meta.fields + ("children",)


class TreeNodeLeavesSerializer(BaseTreeNodeSerializer):
    """For getting leaves only"""

    class Meta(BaseTreeNodeSerializer.Meta):
        model = TreeNode
        fields = ("name", "info") + tuple(settings.PROFILES_SERIALIZERS.keys())
        depth = 1


class IdTreeNodeSerializer(serializers.ModelSerializer):
    def build_nested_field(self, field_name, relation_info, nested_depth):
        if SERIALIZERS.get(field_name) is not None:
            return SERIALIZERS.get(field_name), {"many": True, "required": False}

        return self.build_relational_field(field_name, relation_info)

    class Meta:
        model = TreeNode
        fields = ("id", "name", "info", "children", "level") + tuple(
            settings.PROFILES_SERIALIZERS.keys()
        )
        depth = 1


class NestedTreeNodeSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        data = super().to_representation(instance)

        # Assume leaves are the only nodes that have profiles
        if not instance.get_children().exists():
            # Add profile data for this node
            for profile_type in SERIALIZERS.keys():
                model = SERIALIZERS[profile_type].Meta.model
                if hasattr(model, "get_optimized_queryset"):
                    profiles = model.get_optimized_queryset().filter(tree_node=instance)
                else:
                    profiles = model.objects.filter(tree_node=instance)
                data[profile_type] = SERIALIZERS[profile_type](
                    profiles, many=True, context=self.context
                ).data

        # Handle children using MPTT's get_children()
        else:
            children = instance.get_children()
            data["children"] = self.__class__(
                children, many=True, context=self.context
            ).data

        return data

    class Meta:
        model = TreeNode
        fields = ("name", "info", "children", "level") + tuple(
            settings.PROFILES_SERIALIZERS.keys()
        )
        depth = 2


class LeavesWithProfilesSerializer(serializers.ModelSerializer):
    has_children = serializers.SerializerMethodField()

    def get_has_children(self, obj):
        return obj.get_children().exists()

    def build_nested_field(self, field_name, relation_info, nested_depth):
        if SERIALIZERS.get(field_name) is not None:
            return SERIALIZERS.get(field_name), {"many": True, "required": False}

        return super(LeavesWithProfilesSerializer, self).build_nested_field(
            field_name, relation_info, nested_depth
        )

    class Meta:
        model = TreeNode
        fields = ("id", "name", "info", "level", "parent", "has_children") + tuple(
            settings.PROFILES_SERIALIZERS.keys()
        )
        depth = 1
