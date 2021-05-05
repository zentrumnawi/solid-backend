from django.conf import settings
from django.core.mail import send_mail
from rest_framework import generics, response, status

from .serializers import ContactSerializer


class ContactView(generics.GenericAPIView):
    serializer_class = ContactSerializer

    permission_classes = ()

    def post(self, request, *args, **kwargs):
        serializer = ContactSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data

        message = send_mail(
            subject=data["subject"],
            message=data["message"],
            from_email="{0} <{1}>".format(data["name"], data["email"]),
            recipient_list=[settings.SYSTEM_EMAIL],
            fail_silently=False,
        )
        if not message:
            return response.Response(status=status.HTTP_400_BAD_REQUEST)
        return response.Response(data=data)
