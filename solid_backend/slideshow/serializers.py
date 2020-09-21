from rest_framework import serializers

from solid_backend.photograph.serializers import PhotographSerializer

from .models import Slideshow, SlideshowImage, SlideshowPage


class SlideshowImageLessSerializer(serializers.ModelSerializer):
    img = PhotographSerializer()

    class Meta:
        model = SlideshowImage
        fields = ["id", "position", "title", "img", "caption"]


class SlideshowPageLessSerializer(serializers.ModelSerializer):
    images = SlideshowImageLessSerializer(many=True)

    class Meta:
        model = SlideshowPage
        fields = ["id", "position", "title", "text", "images"]


class SlideshowSerializer(serializers.ModelSerializer):
    img = PhotographSerializer()
    pages = SlideshowPageLessSerializer(many=True)

    class Meta:
        model = Slideshow
        fields = "__all__"


class SlideshowPageSerializer(serializers.ModelSerializer):
    images = SlideshowImageLessSerializer(many=True)

    class Meta:
        model = SlideshowPage
        fields = "__all__"


class SlideshowImageSerializer(serializers.ModelSerializer):
    img = PhotographSerializer()

    class Meta:
        model = SlideshowImage
        fields = "__all__"
