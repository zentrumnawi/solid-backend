from django.db import models


class Slideshow(models.Model):
    """
    Model for a series of pages that can be switched back and forth.
    """

    active = models.BooleanField(default=True)
    position = models.PositiveSmallIntegerField()
    title = models.CharField(max_length=100)
    title_image = models.OneToOneField(
        to="photograph.Photograph", on_delete=models.PROTECT, null=True, blank=True
    )

    def __str__(self):
        return self.title


class SlideshowPage(models.Model):
    """
    Model for a page of the Slideshow model.
    """

    show = models.ForeignKey(
        to=Slideshow,
        on_delete=models.PROTECT,
        related_name="pages",
        related_query_name="page",
        db_index=False,
    )
    position = models.PositiveSmallIntegerField()
    title = models.CharField(max_length=100)
    text = models.TextField(verbose_name="text (Markdown)")

    def __str__(self):
        return self.title


class SlideshowImage(models.Model):
    """
    Model for an image for a page of the Slideshow model.
    """

    page = models.ForeignKey(
        to=SlideshowPage,
        on_delete=models.CASCADE,
        related_name="images",
        related_query_name="image",
        db_index=False,
    )
    position = models.PositiveSmallIntegerField()
    title = models.CharField(max_length=100)
    image = models.ForeignKey(
        to="photograph.Photograph", on_delete=models.CASCADE, null=True, blank=True
    )
    caption = models.TextField(
        default="", blank=True, verbose_name="caption (Markdown)"
    )

    def __str__(self):
        return str(self.image)
