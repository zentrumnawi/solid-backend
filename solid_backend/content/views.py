from django.conf import settings
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import TreeNode
from .serializers import TreeNodeSerializer


class ProfileEndpoint(ReadOnlyModelViewSet):
    """
    Endpoint that provides the database table of the tree structure of all profiles with their related photographs
    """

    queryset = TreeNode.objects.root_nodes()
    serializer_class = TreeNodeSerializer
    name = "profile"
