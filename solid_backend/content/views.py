from django.db.models import Prefetch, F
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
import logging

from solid_backend.media_object.models import MediaObject

from .models import TreeNode
from .serializers import (
    TreeNodeSerializer,
    TreeNodeDetailSerializer,
    TreeNodeListSerializer,
    TreeNodeChildrenSerializer,
    TreeNodeParentSerializer,
    TreeNodeLeavesSerializer,
)

# logger = logging.getLogger(__name__)
logger = logging.getLogger(__name__)


class ProfileEndpoint(ReadOnlyModelViewSet):
    """
    Endpoint that provides the database table of the tree structure of all profiles with their related photographs
    """

    serializer_class = TreeNodeSerializer
    name = "profile"

    def get_queryset(self):
        if not hasattr(TreeNode, "profiles"):
            logger.debug("No profiles found on TreeNode model!!!!!!!!!!!!!!!!!")
            return TreeNode.objects.root_nodes()

        # Get the deepest level of the tree structure.
        level_max = 0
        logger.debug("Profiles !!!!!!!!!!!!!!!!!!")

        for obj in TreeNode.objects.only("level"):
            if level_max < obj.level:
                level_max = obj.level

        # Generate a list of lookups for the profiles with their related photographs
        # ordered by their profile_positions up to level_max in the tree structure.
        lookup = "profiles__media_objects"
        queryset = MediaObject.objects.order_by("profile_position")
        lookup_list = [Prefetch(lookup, queryset=queryset)]

        for i in range(level_max):
            lookup = "children__" + lookup
            lookup_list.append(Prefetch(lookup, queryset=queryset))

        return TreeNode.objects.root_nodes().prefetch_related(*lookup_list)


class RootNodeEndpoint(ReadOnlyModelViewSet):
    queryset = TreeNode.objects.root_nodes()
    serializer_class = TreeNodeListSerializer
    name = "rootnode"


class LeavesEndpoint(ReadOnlyModelViewSet):
    queryset = TreeNode.objects.filter(lft=F("rght") - 1)
    serializer_class = TreeNodeLeavesSerializer
    name = "leaves"


class ChildrenEndpoint(ReadOnlyModelViewSet):
    queryset = TreeNode.objects.all()
    serializer_class = TreeNodeChildrenSerializer
    name = "children"


class ParentNodeEndpoint(ReadOnlyModelViewSet):
    queryset = TreeNode.objects.all()
    serializer_class = TreeNodeParentSerializer
    name = "parentnode"

    def retrieve(self, request, *args, **kwargs):
        node = self.get_object()
        logger.debug(f"Parent node: {node.parent}")
        if not node.parent:
            return Response([])

        serializer = self.get_serializer(node.parent)
        return Response(serializer.data)


class ChildrenEndpoint(ReadOnlyModelViewSet):
    """
    Endpoint that provides the direct children of a specified node.
    """

    queryset = TreeNode.objects.all()
    serializer_class = TreeNodeChildrenSerializer
    name = "children"

    def retrieve(self, request, *args, **kwargs):
        try:
            node = self.get_object()
            children = node.get_children()  # MPTT method to get direct children

            if not children.exists():
                return Response([])
            serializer = self.get_serializer(children, many=True)
            return Response(serializer.data)
        except TreeNode.DoesNotExist:
            return Response({"detail": "Node not found"}, status=404)
