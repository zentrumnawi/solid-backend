from django.db.models import Prefetch, F
from rest_framework.response import Response
from rest_framework.decorators import action
import logging
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError, ParseError
from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet
from django.db.models import Q
from django.conf import settings
import logging
from importlib import import_module
from solid_backend.media_object.models import MediaObject
from mptt.fields import TreeForeignKey

from .models import TreeNode
from .serializers import (
    TreeNodeDetailSerializer,
    TreeNodeListSerializer,
    TreeNodeChildrenSerializer,
    TreeNodeParentSerializer,
    TreeNodeLeavesSerializer,
    NestedTreeNodeSerializer,
    LeavesWithProfilesSerializer,
    IdTreeNodeSerializer,
    SERIALIZERS
)

# logger = logging.getLogger(__name__)
logger = logging.getLogger(__name__)


class NestedProfileEndpoint(ReadOnlyModelViewSet):
    """
    Endpoint that provides the database table of the tree structure of all profiles.
    """

    serializer_class = NestedTreeNodeSerializer
    name = "profile"

    def get_queryset(self):
        if not hasattr(TreeNode, "profiles"):
            return TreeNode.objects.root_nodes()

        # Get the deepest level of the tree structure.
        level_max = 0

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
    serializer_class = LeavesWithProfilesSerializer
    name = "leaves"

class AllNodesFlatEndpoint(ReadOnlyModelViewSet):
    queryset = TreeNode.objects.all()
    serializer_class = LeavesWithProfilesSerializer
    name = "all-nodes-flat"

    def retrieve(self, request, *args, **kwargs):
        
            node = self.get_root()
            nodes = node.get_descendants(include_self=True)  # MPTT method to get direct children

            serializer = self.get_serializer(nodes, many=True)
            return Response(serializer.data)

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

# curl -X GET http://localhost:8000/recursive/profiles/ | python -m json.tool
# curl -X GET http://localhost:8000/recursive/profiles/?level=1 | python -m json.tool
class IdListProfileEndpoint(ReadOnlyModelViewSet):
    """
    Endpoint returning the profile tree.
    """

    serializer_class = IdTreeNodeSerializer
    queryset = TreeNode.objects.all()
    name = "profile"
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["level", "parent"]

    @action(
        detail=False,
        url_name="root",
        url_path="root",
    )
    def root(self, request, *args, **kwargs):
        queryset = TreeNode.objects.root_nodes()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

# curl -X GET http://localhost:8000/contentItem/wine_related/ | python -m json.tool
# curl -X GET http://localhost:8000/contentItem/1/wine_related/ | python -m json.tool
class ContentItemEndpoint(GenericViewSet):
    name = "contentItem"
    related_name = ""

    @action(
        detail=True,
        url_name="detail-content-item",
        url_path="(?P<related_name>[a-zA-Z_]*)",
    )
    def detail_content_item(self, request, related_name, *args, **kwargs):
        self.set_model_related_name(related_name)
        self.check_related_name_exists()
        obj = self.get_object()
        serializer = self.get_serializer(obj)
        return Response(data=serializer.data)

    @action(
        detail=False,
        url_name="list-content-item",
        url_path="(?P<related_name>[a-zA-Z_]*)",
    )
    def list_content_item(self, request, related_name, *args, **kwargs):
        self.set_model_related_name(related_name)
        self.check_related_name_exists()
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(data=serializer.data)

    def get_queryset(self):
        model = self.get_model_class(self.related_name)
        return model.objects.all()

    def get_serializer_class(self, *args, **kwargs):
        return SERIALIZERS.get(self.related_name, None)

    def get_model_class(self, related_name):
        return self.get_serializer_class(related_name=self.related_name).Meta.model

    def set_model_related_name(self, related_name):
        self.related_name = related_name

    def check_related_name_exists(self):
        if self.related_name not in SERIALIZERS:
            raise ParseError(f"The requested contentItem model {self.related_name} does not exist.")
