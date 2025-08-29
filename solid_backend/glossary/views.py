from django.db.models import Prefetch
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import GlossaryEntry
from .serializers import GlossaryEntrySerializer
import logging
from collections import defaultdict
from rest_framework.response import Response

logger = logging.getLogger(__name__)


class GlossaryEntryEndpoint(ReadOnlyModelViewSet):
    def get_queryset(self):
        return GlossaryEntry.objects.all().prefetch_related(
            Prefetch("links", queryset=GlossaryEntry.objects.order_by("term"))
        )

    def list(self, request):
        response_data = defaultdict(list)
        queryset = self.get_queryset()

        serialized = GlossaryEntrySerializer(
            queryset, many=True, context={"request": request}
        ).data
        for item in serialized:
            response_data[item["tags"]].append(item)
        return Response(response_data)

    serializer_class = GlossaryEntrySerializer
    name = "glossaryentry"
