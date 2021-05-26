from datetime import date
from os import makedirs, path
from shutil import rmtree

import django.db.models.options as options
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.forms import FileField, ImageField
from django.utils.translation import ugettext_lazy as _
from stdimage.models import JPEGField, JPEGFieldFile, StdImageField

from solid_backend.openzoom import deepzoom

from .forms import MediaObjectFormField

options.DEFAULT_NAMES = options.DEFAULT_NAMES + ("image_field_name",)


class DeepZoom(models.Model):
    """
    Abstract Model for creation of Deep Zoom images
    """

    dzi_option = models.BooleanField(default=False, verbose_name="Deep Zoom option")
    dzi_file = models.FileField(
        null=True, editable=False, verbose_name="Deep Zoom file", max_length=200
    )

    def create_deepzoom_files(self, upload_to="dzi"):
        # Generate Deep Zoom directory and file name form the image file name.
        image_absolute_path_file = getattr(self, self._meta.image_field_name).path
        slug = path.basename(image_absolute_path_file).split(".")[0]
        dzi_file_name = slug + ".dzi"
        dzi_absolute_path = path.join(settings.MEDIA_ROOT, upload_to, slug)
        dzi_absolute_path_file = path.join(dzi_absolute_path, dzi_file_name)
        dzi_relative_path_file = path.join(upload_to, slug, dzi_file_name)

        if self.dzi_file:
            if self.dzi_file.name == dzi_relative_path_file:
                return  # No update
            else:
                # Delete existing Deep Zoom directory before update.
                self.delete_deepzoom_files()

        # Create Deep Zoom image files.
        makedirs(dzi_absolute_path)
        creator = deepzoom.ImageCreator(
            tile_size=254,
            tile_overlap=1,
            tile_format="jpg",
            image_quality=0.9,
            resize_filter="antialias",
        )
        creator.create(image_absolute_path_file, dzi_absolute_path_file)
        self.dzi_file = dzi_relative_path_file

    def delete_deepzoom_files(self):
        rmtree(path.dirname(self.dzi_file.path))
        self.dzi_file = None

    def save(self, *args, **kwargs):
        if self.dzi_option:
            super().save(*args, **kwargs)  # Get image file path.
            self.create_deepzoom_files()
        elif self.dzi_file:
            self.delete_deepzoom_files()

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.dzi_file:
            self.delete_deepzoom_files()
        super().delete(*args, **kwargs)

    class Meta:
        abstract = True
        # An option 'image_field_name' must be set in the child class.


class MediaObjectFieldFile(JPEGFieldFile):
    def render_variations(self, replace=True):
        if self.instance.media_format == "image":
            super(MediaObjectFieldFile, self).render_variations(replace)

    def delete_variations(self):
        if self.instance.media_format == "image":
            super(MediaObjectFieldFile, self).delete_variations()


class MediaObjectField(StdImageField):
    """
    A JPEGFieldField which acts like JPEGFieldField if the provided media
    is of image type and in other cases as FileField.
    """

    attr_class = MediaObjectFieldFile

    def formfield(self, **kwargs):
        return super().formfield(**{"form_class": MediaObjectFormField, **kwargs,})


class MediaObject(DeepZoom):
    """
    Model for a photograph.
    """

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(default=0)
    profile = GenericForeignKey("content_type", "object_id")
    profile_position = models.PositiveSmallIntegerField(null=True, blank=True)

    media_format = models.CharField(
        max_length=5,
        choices=(("image", _("image")), ("audio", _("audio")), ("video", _("video")),),
        verbose_name=_("media format"),
    )

    file = MediaObjectField(
        upload_to="media_object/",
        width_field="img_original_width",
        height_field="img_original_height",
        variations={
            "large": (1200, None),
            "medium": (900, None),
            "small": (600, None),
            "thumbnail": (100, 100, True),
        },
        db_index=True,
        delete_orphans=True,
    )

    img_original_width = models.PositiveSmallIntegerField(
        editable=False, null=True, blank=True, verbose_name="img width"
    )
    img_original_height = models.PositiveSmallIntegerField(
        editable=False, null=True, blank=True, verbose_name="img height"
    )
    img_original_scale = models.FloatField(verbose_name="scale", null=True, blank=True)

    img_alt = models.CharField(
        max_length=200, null=True, blank=True, verbose_name=_("alternative text")
    )

    description = models.TextField(
        default="", null=True, blank=True, verbose_name="description (Markdown)"
    )
    audio = models.FileField(upload_to="audio/", null=True, blank=True)

    title = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name=_("title of image/audio/video file"),
    )

    date = models.DateField(null=True, blank=True, help_text=_("Date of creation"))
    author = models.CharField(max_length=100, default="", blank=True)
    license = models.CharField(max_length=100, default="", blank=True)

    def __str__(self):
        return str(self.file)

    class Meta:
        image_field_name = "file"


class ImageManager(models.Manager):
    def get_queryset(self):
        return super(ImageManager, self).get_queryset().filter(media_format="image")


class AudioVideoManager(models.Manager):
    def get_queryset(self):
        return (
            super(AudioVideoManager, self).get_queryset().exclude(media_format="image")
        )


class ImageMediaObject(MediaObject):

    objects = ImageManager()

    class Meta:
        proxy = True


class AudioVideoMediaObject(MediaObject):

    objects = AudioVideoManager()

    class Meta:
        proxy = True
