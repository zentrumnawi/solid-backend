from rest_framework import serializers
from django.db.models import TextField


# Module designed for use of optional dependency drf-spectacular Schema

SPECTACULAR_INSTALLED = True

try:
    import drf_spectacular.extensions as extensions

except ImportError:
    pass

else:
    class MDTextField(TextField):
        """
        Model field to declare markdown compatible fields.
        """
        pass


    class MDSerializerField(serializers.CharField):
        """
        Serializer field to provide a mapping which can bedetected by the MdFieldExtension.
        """
        pass


    class MdFieldExtension(extensions.OpenApiSerializerFieldExtension):
        target_class = "solid_backend.utils.drf_spectacluar_extensions.MDSerializerField"

        def map_serializer_field(self, auto_schema, direction):
            schema = auto_schema._map_serializer_field(self.target, direction, bypass_extensions=True)
            schema['format'] = 'mdstring'
            return schema


    class TitleSerializerExtension(extensions.OpenApiSerializerExtension):
        target_class = "solid_backend.utils.serializers.SolidModelSerializer"
        match_subclasses = True

        def map_serializer(self, auto_schema, direction):
            schema = auto_schema._map_serializer(self.target, direction, bypass_extensions=True)
            ser_meta = getattr(self.target, "Meta", None)
            title = ser_meta.model._meta.verbose_name
            if ser_meta and title:
                schema["title"] = title
            return schema
