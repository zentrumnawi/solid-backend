from django.db.models import Prefetch
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import GlossaryEntry
from .serializers import GlossaryEntrySerializer


class GlossaryEntryEndpoint(ReadOnlyModelViewSet):
    """
    Endpoint that provides the database table of all glossary entries.
    """

    queryset = GlossaryEntry.objects.all().prefetch_related(
        Prefetch("links", queryset=GlossaryEntry.objects.order_by("term"))
    )
    serializer_class = GlossaryEntrySerializer
    name = "glossaryentry"
