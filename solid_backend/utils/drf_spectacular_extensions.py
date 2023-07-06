import re
import django
from drf_spectacular.hooks import postprocess_schema_enums
from drf_spectacular.settings import spectacular_settings
from rest_framework import serializers
from django.db.models import TextField


# Module designed for use of optional dependency drf-spectacular Schema

SPECTACULAR_INSTALLED = True

try:
    import drf_spectacular.extensions as extensions

except ImportError:
    SPECTACULAR_INSTALLED = False
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


    def postprocess_choice_field_type(result, generator, request, public):
        """
        Post-Processing Hook that appends the type of the enum items to the initial prop schema.
        """

        def iter_prop_containers(schema, component_name=None):
            if not component_name:
                for component_name, schema in schema.items():
                    if spectacular_settings.COMPONENT_SPLIT_PATCH:
                        component_name = re.sub('^Patched(.+)', r'\1', component_name)
                    if spectacular_settings.COMPONENT_SPLIT_REQUEST:
                        component_name = re.sub('(.+)Request$', r'\1', component_name)
                    yield from iter_prop_containers(schema, component_name)
            elif isinstance(schema, list):
                for item in schema:
                    yield from iter_prop_containers(item, component_name)
            elif isinstance(schema, dict):
                if schema.get('properties'):
                    yield component_name, schema['properties']
                yield from iter_prop_containers(schema.get('oneOf', []), component_name)
                yield from iter_prop_containers(schema.get('allOf', []), component_name)
                yield from iter_prop_containers(schema.get('anyOf', []), component_name)

        schemas = result.get('components', {}).get('schemas', {})
        for component_name, props in iter_prop_containers(schemas):
            for prop_name, prop_schema in props.items():
                ref_name = ""
                if "$ref" in prop_schema:
                    ref_name = prop_schema["$ref"]
                if "allOf" in prop_schema:
                    ref_name = prop_schema["allOf"][0]["$ref"]
                if "oneOf" in prop_schema:
                    ref_name = prop_schema["oneOf"][0]["$ref"]
                if "Enum" in ref_name:
                    prop_schema["type"] = schemas.get(ref_name.rsplit("/", 1)[1])["type"]

        return result
