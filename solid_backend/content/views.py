from django.db.models import Prefetch
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from solid_backend.media_object.models import MediaObject

from .models import TreeNode
from .serializers import NestedTreeNodeSerializer, IdTreeNodeSerializer


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


