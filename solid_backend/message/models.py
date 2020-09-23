from datetime import date

from django.db import models


class Message(models.Model):
    """
    Model for a message that is displayed to the users when the app starts.
    """

    MTYPE_CHOICES = [("CL", "Changelog"), ("SE", "Series"), ("NO", "Notice")]

    type = models.CharField(max_length=2, choices=MTYPE_CHOICES)
    title = models.CharField(max_length=100)
    text = models.TextField(default="", blank=True, verbose_name="text (Markdown)")
    img = models.ForeignKey(
        to="photograph.Photograph", on_delete=models.PROTECT, null=True, blank=True
    )
    valid_from = models.DateField(default=date.today)
    valid_to = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title
