from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import Photograph
from .serializers import PhotographSerializer


class PhotographEndpoint(ReadOnlyModelViewSet):
    """
    Endpoint that provides the database table of all photographs.
    """

    queryset = Photograph.objects.all()
    serializer_class = PhotographSerializer
    name = "photograph"
