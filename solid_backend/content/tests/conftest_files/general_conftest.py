import pytest

from solid_backend.content.models import BaseProfile, TreeNode


@pytest.fixture
def base_profile_model_class():
    return BaseProfile


@pytest.fixture
def tree_node_model_class():
    return TreeNode
