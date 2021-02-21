from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from mptt.models import TreeForeignKey


class TestBaseProfileModelExists:
    """
    Test whether an object BaseProfile can be imported and is a Django model.
    """

    def test_model_exists(self):
        pass

    def test_model_is_django_model(self):
        from solid_backend.content.models import BaseProfile

        assert issubclass(BaseProfile, models.Model)


class TestBaseProfileModelFields:
    """
    Test suite with basic field tests whether all fields of the BaseProfile object
    exist and have the correct class instance and field attribute values.
    """

    def test_model_has_field_photographs(self, base_profile_model_class):
        assert hasattr(base_profile_model_class, "photographs")

    def test_model_has_field_tree_node(self, base_profile_model_class):
        assert hasattr(base_profile_model_class, "tree_node")

    def test_field_type_photographs(self, base_profile_model_class):
        assert isinstance(
            base_profile_model_class._meta.get_field("photographs"), GenericRelation
        )

    def test_field_type_tree_node(self, base_profile_model_class):
        assert isinstance(
            base_profile_model_class._meta.get_field("tree_node"), TreeForeignKey
        )

    def test_field_attribute_values_tree_node(
        self, base_profile_model_class, tree_node_model_class
    ):
        field = base_profile_model_class._meta.get_field("tree_node")
        assert issubclass(field.related_model, tree_node_model_class)


class TestTreeNodeModelExists:
    """
    Test whether an object TreeNode can be imported and is a Django model.
    """

    def test_model_exists(self):
        pass

    def test_model_is_django_model(self):
        from solid_backend.content.models import TreeNode

        assert issubclass(TreeNode, models.Model)


class TestTreeNodeModelFields:
    """
    Test suite with basic field tests whether all fields of the TreeNode object exist
    and have the correct class instance and field attribute values.
    """

    def test_model_has_field_parent(self, tree_node_model_class):
        assert hasattr(tree_node_model_class, "parent")

    def test_model_has_field_name(self, tree_node_model_class):
        assert hasattr(tree_node_model_class, "name")

    def test_model_has_field_info(self, tree_node_model_class):
        assert hasattr(tree_node_model_class, "info")

    def test_field_type_parent(self, tree_node_model_class):
        assert isinstance(
            tree_node_model_class._meta.get_field("parent"), TreeForeignKey
        )

    def test_field_type_name(self, tree_node_model_class):
        assert isinstance(
            tree_node_model_class._meta.get_field("name"), models.CharField
        )

    def test_field_type_info(self, tree_node_model_class):
        assert isinstance(
            tree_node_model_class._meta.get_field("info"), models.TextField
        )
