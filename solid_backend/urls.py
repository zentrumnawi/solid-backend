from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

urlpatterns = [
    path("", include("solid_backend.contact.urls")),
    path("", include("solid_backend.content.urls")),
    path("", include("solid_backend.glossary.urls")),
    path("", include("solid_backend.message.urls")),
    path("", include("solid_backend.photograph.urls")),
    path("", include("solid_backend.quiz.urls")),
    path("", include("solid_backend.slideshow.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
