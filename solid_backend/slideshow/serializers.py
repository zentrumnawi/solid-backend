from rest_framework import serializers

from solid_backend.photograph.serializers import PhotographSerializer
from solid_backend.utils.serializers import DynamicExcludeModelSerializer

from .models import Slideshow, SlideshowImage, SlideshowPage


class SlideshowImageSerializer(DynamicExcludeModelSerializer):
    image = PhotographSerializer()

    class Meta:
        model = SlideshowImage
        fields = "__all__"


class SlideshowPageSerializer(DynamicExcludeModelSerializer):
    images = SlideshowImageSerializer(exclude="page", many=True)

    class Meta:
        model = SlideshowPage
        fields = "__all__"


class SlideshowSerializer(serializers.ModelSerializer):
    title_image = PhotographSerializer()
    pages = SlideshowPageSerializer(exclude="show", many=True)

    class Meta:
        model = Slideshow
        exclude = ["active"]
