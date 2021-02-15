from django.db import models


class TestTreeNodeModelExists:
    """
    Test whether an object TreeNode can be imported and is a Django model.
    """

    def test_model_exists(self):
        pass

    def test_model_is_django_model(self):
        from solid_backend.content.models import TreeNode

        assert issubclass(TreeNode, models.Model)
