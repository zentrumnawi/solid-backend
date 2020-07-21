from datetime import date

from django.db.models import Q
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Message
from .serializers import MessageSerializer


class MessageEndpoint(ReadOnlyModelViewSet):
    """
    Provide database table of currently valid messages.
    """

    queryset = Message.objects.filter(
        Q(valid_from__lte=date.today(), valid_to__gte=date.today())
        | Q(valid_from__lte=date.today(), valid_to__isnull=True)
    )
    serializer_class = MessageSerializer
    name = "message"
