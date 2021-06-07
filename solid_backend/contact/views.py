from django.conf import settings
from django.core.mail import EmailMessage
from rest_framework import generics, response, status

from .serializers import ContactSerializer


def format_message(url, name, email, message):
    text = (
        f"Name: {name}",
        f"E-Mail: {email}",
        "Nachricht:",
        "",
        message,
        "",
        "---------",
        "",
        f"Das ist eine automatisch generierte Nachricht (System URL: {url})",
    )

    return "\n".join(text)


class ContactView(generics.GenericAPIView):
    serializer_class = ContactSerializer

    permission_classes = ()

    def post(self, request, *args, **kwargs):
        serializer = ContactSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data

        message = EmailMessage(
            subject="[{}] {}".format(settings.PROJECT_NAME, data["subject"]),
            body=format_message(
                request.build_absolute_uri(),
                data["name"],
                data["email"],
                data["message"],
            ),
            from_email="Feedback <{}>".format(settings.SYSTEM_EMAIL),
            to=[settings.SYSTEM_EMAIL],
            reply_to=[data["email"],],
        )
        message.send(fail_silently=False)

        if not message:
            return response.Response(status=status.HTTP_400_BAD_REQUEST)

        return response.Response(data=data)
