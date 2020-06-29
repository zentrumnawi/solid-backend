from django.urls import path, include

urlpatterns = [
    path("", include("solid_backend.contact.urls")),
    path("", include("solid_backend.content.urls")),
    path("", include("solid_backend.glossary.urls")),
    path("", include("solid_backend.message.urls")),
    path("", include("solid_backend.quiz.urls")),
    path("", include("solid_backend.slideshow.urls")),
]
