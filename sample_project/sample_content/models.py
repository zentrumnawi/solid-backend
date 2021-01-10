from django.db import models

from solid_backend.content.models import BaseProfile, TreeNode
from solid_backend.content.fields import ConcatCharField, FromToConcatField

# Create your models here.


class MyProfile(BaseProfile):
    name = models.CharField(max_length=200, default="")
    # my_concat = ConcatCharField(
    #     max_length=600,
    #     concat_choices=[
    #         [(None, "---------"), (1, 1), (2, 2), (3, 3), (4, 4)],
    #         [(None, "---------"), ("Bonbon/s", "Bonbon/s"), ("Tüte/n Popcorn", "Tüte/n Popcorn"), ("Plätzchen", "Plätzchen"), ("Lutscher", "Lutscher")]
    #     ],
    #     seperators=[", ", " und "],
    #     default="",
    #     blank=True
    # )
    # color = FromToConcatField(
    #     max_length=100,
    #     from_choices=[(None, "---------"), ("blau", "blau"), ("grün", "grün"), ("gelb", "gelb"), ("rot", "rot")],
    #     to_choices=[(None, "---------"), ("blau", "blau"), ("grün", "grün"), ("gelb", "gelb"), ("rot", "rot")],
    #     default="",
    #     blank=True,
    # )
    systematics = models.ForeignKey(
        null=True,
        on_delete=models.DO_NOTHING,
        related_name="profiles",
        to=TreeNode,
        verbose_name="Steckbrief-Ebene",
    )
