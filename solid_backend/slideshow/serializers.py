from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from taggit.models import Tag
from taggit.serializers import TagListSerializerField

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
    categories = TagListSerializerField()

    class Meta:
        model = Slideshow
        exclude = ["active"]


class CategoryImageField(serializers.FileField):

    def __init__(self, *args, **kwargs):
        kwargs["source"] = "*"
        super(CategoryImageField, self).__init__(*args, **kwargs)

    def to_representation(self, value):
        """
        Retrieve the thumbnail url of the first SlideShow associated with a tag.
        :param value:
        :return:
        """
        # Since Tags are associated with a SlideShow via
        # a through model TaggedItem which itself has a
        # GenericRelation to the SlideShow things get complicated.
        first_tagged_item = value.taggit_taggeditem_items.first()
        # Get SlideShow ContentType object
        content_type = ContentType.objects.get(id=first_tagged_item.content_type_id)
        image = content_type.get_object_for_this_type(id=first_tagged_item.object_id).title_image.img
        return super(CategoryImageField, self).to_representation(image.thumbnail)


class CategorySerializer(serializers.ModelSerializer):
    image = CategoryImageField()

    class Meta:
        model = Tag
        fields = "__all__"
