from django.db.models import Prefetch
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import GlossaryEntry
from .serializers import GlossaryEntrySerializer
import logging
from collections import defaultdict
from rest_framework.response import Response

logger = logging.getLogger(__name__)

# def get_glossary_entries_by_tag(tag):
#     """
#     Get all glossary entries for a given tag.
#     """
#     return GlossaryEntry.objects.filter(tags=tag)


class GlossaryEntryEndpoint(ReadOnlyModelViewSet):
    """
    Endpoint that provides the database table of all glossary entries.
    """

    queryset = GlossaryEntry.objects.all().prefetch_related(
        Prefetch("links", queryset=GlossaryEntry.objects.order_by("term"))
    )

    def list(self, request):
        response_data = defaultdict(list)
        queryset = self.queryset
        
        serialized = GlossaryEntrySerializer(
            queryset, many=True, context={"request": request}
        ).data
        for item in serialized:
            response_data[item["tags"]].append(item)
        return Response(response_data)


    serializer_class = GlossaryEntrySerializer
    name = "glossaryentry"