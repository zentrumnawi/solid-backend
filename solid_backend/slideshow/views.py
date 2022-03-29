from django.db.models import Prefetch
from rest_framework.viewsets import ReadOnlyModelViewSet
from django_filters import rest_framework as filters
from taggit.models import Tag

from solid_backend.quiz.views import TagsFilter
from .models import Slideshow, SlideshowImage, SlideshowPage
from .serializers import (
    CategorySerializer,
    CompleteSlideshowSerializer,
    MinimalSlideshowSerializer,
    SlideshowImageSerializer,
    SlideshowPageSerializer,
)


class SlideshowFilterSet(filters.FilterSet):
    categories = TagsFilter(field_name="categories__id")

    class Meta:
        model = Slideshow
        fields = ["categories", ]


class SlideshowEndpoint(ReadOnlyModelViewSet):
    """
    Endpoint that provides the database table of all
    active slideshows including their related pages with their related images.

    The LIST endpoint is modified in the way that it only returns the IDs of
    assotiated SlideShowPages not the complete objects.
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
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = SlideshowFilterSet

    def get_serializer_class(self):
        if self.request.parser_context["view"].detail:
            return CompleteSlideshowSerializer
        return MinimalSlideshowSerializer

    serializer_class = MinimalSlideshowSerializer
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
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ["show", ]


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
