from django.db import models
from stdimage import JPEGField
from datetime import date


class Photograph(models.Model):
    """
    Model for a photograph.
    """

    # profile = models.ForeignKey(to=Profile,
    #    on_delete=models.CASCADE,
    #    related_name="photographs",
    #    related_query_name="photograph",
    # )
    img = JPEGField(
        upload_to="photograph/",
        width_field="img_original_width",
        height_field="img_original_height",
        variations={
            "large": (1200, 800),
            "medium": (900, 600),
            "small": (600, 400),
            "thumbnail": (100, 100, True),
        },
        db_index=True,
        delete_orphans=True,
    )
    # dzi_file = models.FileField(upload_to="dzi_files/", null=True, blank=True, editable=False)
    img_original_width = models.PositiveSmallIntegerField(editable=False)
    img_original_height = models.PositiveSmallIntegerField(editable=False)
    img_original_scale = models.FloatField(verbose_name="scale", null=True, blank=True,)

    img_alt = models.CharField(max_length=200)
    description = models.TextField(
        default="", blank=True, verbose_name="description (Markdown)"
    )
    # audio_file = models.FileField(upload_to="audio_files/", null=True, blank=True)
    # audio_duration = models.PositiveIntegerField(null=True, blank=True, editable=False)

    # location =
    date = models.DateField(
        null=True, blank=True, help_text="Datum der Lichtbildaufnahme"
    )
    author = models.CharField(max_length=100, default="", blank=True)
    license = models.CharField(max_length=100, default="", blank=True)

    def __str__(self):
        return str(self.img)
