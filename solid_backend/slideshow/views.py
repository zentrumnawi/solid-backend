from django.db.models import Prefetch
from rest_framework.viewsets import ReadOnlyModelViewSet
from taggit.models import Tag

from .models import Slideshow, SlideshowImage, SlideshowPage
from .serializers import (
    SlideshowImageSerializer,
    SlideshowPageSerializer,
    SlideshowSerializer,
    CategorySerializer
)


class SlideshowEndpoint(ReadOnlyModelViewSet):
    """
    Endpoint that provides the database table of all active slideshows including their related pages with their related images.
    """

    queryset = (
        Slideshow.objects.filter(active=True)
        .order_by("position")
        .prefetch_related(
            Prefetch(
                "pages",
                queryset=SlideshowPage.objects.order_by("position").prefetch_related(
                    Prefetch(
                        "images", queryset=SlideshowImage.objects.order_by("position")
                    )
                ),
            )
        )
    )

    def get_queryset(self):
        queryset = super(SlideshowEndpoint, self).get_queryset()
        category = self.request.query_params.get("categories")

        if category is not None:
            queryset = queryset.filter(categories=category)

        return queryset

    serializer_class = SlideshowSerializer
    name = "slideshow"


class SlideshowPageEndpoint(ReadOnlyModelViewSet):
    """
    Endpoint that provides the database table of all slideshow pages including their related images.
    """

    queryset = SlideshowPage.objects.order_by("show", "position").prefetch_related(
        Prefetch("images", queryset=SlideshowImage.objects.order_by("position"))
    )
    serializer_class = SlideshowPageSerializer
    name = "slideshowpage"


class SlideshowImageEndpoint(ReadOnlyModelViewSet):
    """
    Endpoint that provides the database table of all slideshow images.
    """

    queryset = SlideshowImage.objects.order_by("page", "position")
    serializer_class = SlideshowImageSerializer
    name = "slideshowimage"


class CategoryEndpoint(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = CategorySerializer
    name = "category"

    def get_queryset(self):
        queryset = super(CategoryEndpoint, self).get_queryset()
        return queryset.filter(slideshow__active=True).distinct()
