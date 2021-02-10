from django.conf import settings
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import TreeNode
from .serializers import TreeNodeSerializer


class ProfilesEndpoint(ReadOnlyModelViewSet):
    model = TreeNode
    queryset = model.objects.root_nodes()
    serializer_class = TreeNodeSerializer
    name = "profiles"
    app = "api"
