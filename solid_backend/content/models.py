import warnings

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.translation import ugettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey

from solid_backend.media_object.models import MediaObject
from solid_backend.photograph.models import Photograph


class TreeNode(MPTTModel):
    """
    Model for a tree structure to repesent the systematics of profiles.
    """

    parent = TreeForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
        related_query_name="child",
    )
    name = models.CharField(max_length=200, unique=True)
    info = models.TextField(max_length=500, blank=True)

    class Meta:
        verbose_name = _("Tree node")
        verbose_name_plural = _("Tree nodes")

    def __str__(self):
        return self.name


def base_profile(*args, **kwargs):

    warnings.warn(
        "BaseProfile is deprecated; use SolidBaseProfile instead.", DeprecationWarning
    )

    class _BaseProfile(models.Model):

        """
        Abstract base model for profiles that provides a relation to the TreeNode model and
        a one-to-many relation to the Photograph model via a generic relation. This base
        model is to be inheriated only once!
        """

        photographs = GenericRelation(Photograph)
        tree_node = TreeForeignKey(
            to=TreeNode,
            on_delete=models.DO_NOTHING,
            null=True,
            related_name="profiles",
            related_query_name="profile",
        )

        class Meta:
            abstract = True

    return _BaseProfile


BaseProfile = base_profile()


class SolidBaseProfile(models.Model):
    """
    Abstract base model for profiles that provides a relation to the TreeNode model and
    a one-to-many relation to the MediaObject model via a generic relation. This base
    model is to be inheriated only once!
    """

    media_objects = GenericRelation(MediaObject)
    tree_node = TreeForeignKey(
        to=TreeNode,
        on_delete=models.DO_NOTHING,
        null=True,
        related_name="profiles",
        related_query_name="profile",
    )

    class Meta:
        abstract = True
