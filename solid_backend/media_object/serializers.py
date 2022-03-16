from rest_framework import serializers

from .models import MediaObject


# Class derived from django-stdimage-serializer 0.1.2
class MediaFileField(serializers.ImageField):
    """
    Get all the variations of the StdImageField
    """

    def to_native(self, obj):
        return self.get_variations_urls(obj)

    def to_representation(self, obj):
        if not obj.path.lower().endswith(("jpg", "jpeg")):
            return {"original": super(MediaFileField, self).to_representation(obj)}
        return self.get_variations_urls(obj)

    def get_variations_urls(self, obj):
        """
        Get all the logo urls.
        """

        # Initiate return object
        return_object = {}

        # Get the field of the object
        field = obj.field

        # A lot of ifs going araound, first check if it has the field variations
        if hasattr(field, "variations"):
            # Get the variations
            variations = field.variations
            # Go through the variations dict
            for key in variations.keys():
                # Just to be sure if the stdimage object has it stored in the obj
                if hasattr(obj, key):
                    # get the by stdimage properties
                    field_obj = getattr(obj, key, None)
                    if field_obj and hasattr(field_obj, "url"):
                        # store it, with the name of the variation type into our return object
                        return_object[key] = super(
                            MediaFileField, self
                        ).to_representation(field_obj)

        # Also include the original (if possible)
        if hasattr(obj, "url"):
            return_object["original"] = super(MediaFileField, self).to_representation(
                obj
            )

        return return_object


class MediaObjectSerializer(serializers.ModelSerializer):
    file = MediaFileField()

    class Meta:
        model = MediaObject
        exclude = ["content_type", "object_id", "dzi_option"]
