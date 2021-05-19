from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import MediaObject
from .serializers import PhotographSerializer


class MediaObjectEndpoint(ReadOnlyModelViewSet):
    """
    Endpoint that provides the database table of all photographs.
    """

    queryset = MediaObject.objects.all()
    serializer_class = PhotographSerializer
    name = "photograph"
