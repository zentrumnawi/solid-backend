from rest_framework import serializers
from django.db.models import TextField


# Module designed for use of optional dependency drf-spectacular Schema

SPECTACULAR_INSTALLED = True

try:
    import drf_spectacular
except ImportError:
    SPECTACULAR_INSTALLED = False


class MDTextField(TextField):
    pass


class MDSerializerField(serializers.CharField):
    pass


if SPECTACULAR_INSTALLED:
    class MdFieldExtension(drf_spectacular.extensions.OpenApiSerializerFieldExtension):
        target_class = "wabe_content.serializers.MDField"

        def map_serializer_field(self, auto_schema, direction):
            schema = auto_schema._map_serializer_field(self.target, direction, bypass_extensions=True)
            schema['format'] = 'mdstring'
            return schema
