from django.db import models

from solid_backend.content.fields import ConcatCharField, FromToConcatField
from solid_backend.content.models import SolidBaseProfile


class SampleProfile(SolidBaseProfile):
    name = models.CharField(max_length=200, default="")
    my_concat = ConcatCharField(
        max_length=600,
        concat_choices=[
            [(None, "---------"), (1, 1), (2, 2), (3, 3), (4, 4)],
            [
                (None, "---------"),
                ("Bonbon/s", "Bonbon/s"),
                ("Tüte/n Popcorn", "Tüte/n Popcorn"),
                ("Plätzchen", "Plätzchen"),
                ("Lutscher", "Lutscher"),
            ],
        ],
        seperators=[", ", " und "],
        default="",
        blank=True,
        verbose_name="My Concat verbose"
    )
    color = FromToConcatField(
        max_length=100,
        from_choices=[
            (None, "---------"),
            ("blau", "blau"),
            ("grün", "grün"),
            ("gelb", "gelb"),
            ("rot", "rot"),
        ],
        to_choices=[
            (None, "---------"),
            ("blau", "blau"),
            ("grün", "grün"),
            ("gelb", "gelb"),
            ("rot", "rot"),
        ],
        default="",
        blank=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "EXAMPLE VERBOSE NAME"


class SecondSampleProfile(SolidBaseProfile):

    name = models.CharField(max_length=200, default="")
    integer = models.IntegerField(default=0)

    def __str__(self):
        return self.name
