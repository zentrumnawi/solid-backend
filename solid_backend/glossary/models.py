from django.db import models


class GlossaryEntry(models.Model):
    """
    Defines a model for an entry in the glossary that is displayed in the app.
    """

    term = models.CharField(max_length=100)
    text = models.TextField(null=True, blank=True, verbose_name="text (Markdown)")
    links = models.ManyToManyField("self", symmetrical=False, blank=True, null=True)

    def __str__(self):
        return self.term

    class Meta:
        ordering = ("term",)
