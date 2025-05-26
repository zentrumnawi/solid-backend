from django.db.models import Prefetch
from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet
from django.db.models import Q
from django.conf import settings
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import SERIALIZERS
from mptt.fields import TreeForeignKey

from solid_backend.media_object.models import MediaObject

from .models import TreeNode
from .serializers import TreeNodeSerializer


class ProfileEndpoint(ReadOnlyModelViewSet):
    """
    Endpoint that provides the database table of the tree structure of all profiles with their related photographs
    """

    serializer_class = TreeNodeSerializer
    name = "profile"

    def get_queryset(self):
        if not hasattr(TreeNode, "profiles"):
            return TreeNode.objects.root_nodes()

        # Get the deepest level of the tree structure.
        level_max = 0

        for obj in TreeNode.objects.only("level"):
            if level_max < obj.level:
                level_max = obj.level

        # Generate a list of lookups for the profiles with their related photographs
        # ordered by their profile_positions up to level_max in the tree structure.
        lookup = "profiles__media_objects"
        queryset = MediaObject.objects.order_by("profile_position")
        lookup_list = [Prefetch(lookup, queryset=queryset)]

        for i in range(level_max):
            lookup = "children__" + lookup
            lookup_list.append(Prefetch(lookup, queryset=queryset))

        return TreeNode.objects.root_nodes().prefetch_related(*lookup_list)


class SearchNodeWithProfilesEndpoint(ReadOnlyModelViewSet):
    """
    Endpoint that returns tree nodes that contain the search term in their general_information__name or general_information__synonyms fields.
    """

    serializer_class = LeavesWithProfilesSerializer
    name = "search-node-with-profiles"

    def get_queryset(self):
        search_term = self.request.query_params.get("q", "")
        if not search_term:
            return TreeNode.objects.none()

        if SERIALIZERS:
            for profile_type in SERIALIZERS:

                model_class = SERIALIZERS[profile_type].Meta.model
                # Get the related query name from the model's TreeNode field
                for field in model_class._meta.fields:
                    if (
                        isinstance(field, TreeForeignKey)
                        and field.remote_field.model == TreeNode
                    ):
                        related_query_name = field.related_query_name()

                return TreeNode.objects.filter(
                    Q(
                        **{
                            f"{related_query_name}__general_information__name__icontains": search_term,
                            f"{related_query_name}__general_information__synonyms__icontains": search_term,
                        }
                    )
                ).distinct()
        return TreeNode.objects.none()

    @action(detail=False, methods=["get"])
    def search(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ProfileSearchEndpoint(GenericViewSet):
    """
    Endpoint that searches across all profile types and returns their native serialized data.
    """

    name = "profile-search"

    def get_queryset(self):
        search_term = self.request.query_params.get("q", "")
        if not search_term:
            return []

        results = []
        if SERIALIZERS:
            for profile_type in SERIALIZERS:
                model = SERIALIZERS[profile_type].Meta.model
                profile_results = model.objects.filter(
                    # Q(general_information__sub_name__icontains=search_term) |
                    Q(general_information__name__icontains=search_term)
                )
                if profile_results.exists():
                    results.extend(profile_results)

        return results

    def get_serializer_class(self):
        return SERIALIZERS.get(self.related_name, None)

    def get_serializer_for_model(self, model_name):
        for serializer_name, serializer_class in SERIALIZERS.items():
            if serializer_class.Meta.model.__name__.lower() == model_name.lower():
                return serializer_class
        return None

    @action(detail=False, methods=["get"])
    def search(self, request):
        queryset = self.get_queryset()
        response_data = []
        for item in queryset:
            model_name = item._meta.model_name
            serializer_class = self.get_serializer_for_model(model_name)
            if serializer_class:
                serializer = serializer_class(item, context={'request': request})
                data = serializer.data
                data["def_type"] = model_name
                response_data.append(data)

        return Response(response_data)
