from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.translation import ugettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey

from solid_backend.photograph.models import Photograph

# Custom Models, representing the actual data of a profile, implement here.
# At least one model needs to have a ForeignKey field to the TreeNode model
# with related_name="profiles". If not, the profiles endpoint will throw an
# error.


class BaseProfile(models.Model):
    """
    A base model used for inharitance such that we have a Generic Many (Photograph) to One (Profile)
    Relation.
    """

    photographs = GenericRelation(Photograph, null=True)

    class Meta:
        abstract = True


# Model for the tree representation of the profiles
class TreeNode(MPTTModel):
    parent = TreeForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="leaf_nodes",
    )
    name = models.CharField(max_length=200, verbose_name=_("node name"), unique=True)
    info = models.TextField(max_length=500, blank=True)

    class Meta:
        verbose_name = _("Tree Node")
        verbose_name_plural = _("Tree Nodes")

    def __str__(self):
        return self.name
