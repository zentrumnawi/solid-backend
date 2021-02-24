from rest_framework import serializers


class DynamicExcludeModelSerializer(serializers.ModelSerializer):
    """
    ModelSerializer that takes an additional 'exclude' argument with fields which should
    not be displayed from the automatically generated fields.
    """

    def __init__(self, *args, **kwargs):
        # Instantiate the superclass without the 'exclude' keyword argument
        exclude = kwargs.pop("exclude", None)
        super().__init__(*args, **kwargs)

        # Exclude fields from serializer
        if exclude is not None:
            for field in set(self.fields):
                if field in exclude:
                    self.fields.pop(field)


class RecursiveSerializer(serializers.Serializer):
    """
    Serializer that represents a self-referential field recursively.
    """

    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data
