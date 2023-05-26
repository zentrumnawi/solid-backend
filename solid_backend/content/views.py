from django.db.models import Prefetch
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError, ParseError
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet

from solid_backend.media_object.models import MediaObject

from .models import TreeNode
from .serializers import NestedTreeNodeSerializer, IdTreeNodeSerializer, SERIALIZERS


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


class ContentItemEndpoint(GenericViewSet):
    name = "contentItem"
    related_name = ""

    @action(
        detail=True,
        url_name="detail-content-item",
        url_path="(?P<related_name>[a-zA-Z_]*)",
    )
    def detailContentItem(self, request, related_name, *args, **kwargs):
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
    def listContentItem(self, request, related_name, *args, **kwargs):
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
            raise ParseError("The requested contentItem model does not exist.")
