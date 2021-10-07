from rest_framework import serializers
from taggit.models import Tag
from solid_backend.photograph.serializers import PhotographSerializer
from solid_backend.utils.serializers import DynamicExcludeModelSerializer

from .models import Slideshow, SlideshowImage, SlideshowPage


class SlideshowImageSerializer(DynamicExcludeModelSerializer):
    image = PhotographSerializer()

    class Meta:
        model = SlideshowImage
        fields = "__all__"


class SlideshowPageSerializer(DynamicExcludeModelSerializer):
    images = SlideshowImageSerializer(exclude="page", many=True, required=False)

    class Meta:
        model = SlideshowPage
        fields = "__all__"


class SlideshowSerializer(serializers.ModelSerializer):
    title_image = PhotographSerializer(required=False)
    pages = SlideshowPageSerializer(exclude="show", many=True, required=False)

    class Meta:
        model = Slideshow
        exclude = ["active"]


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = "__all__"
