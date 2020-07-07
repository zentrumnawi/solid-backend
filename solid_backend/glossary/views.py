from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import GlossaryEntry
from .serializers import GlossaryEntrySerializer


class GlossaryEntryEndpoint(ReadOnlyModelViewSet):
    """
    Endpoint that provides the database table of all glossary entries.
    """

    queryset = GlossaryEntry.objects.all()
    serializer_class = GlossaryEntrySerializer
    name = "glossaryentry"
