import pytest

from solid_backend.content.models import TreeNode


@pytest.fixture
def tree_node_model_class():
    return TreeNode
