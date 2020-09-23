from os import path

import django.db.models.deletion
from django.db import migrations, models
from django.db.models import Q
from stdimage.models import JPEGFieldFile


def change_img_field(apps, schema_editor):
    """
    Replace image file with a relation to a photograph instance created from the image.
    """
    Slideshow = apps.get_model("slideshow", "Slideshow")
    Photograph = apps.get_model("photograph", "Photograph")

    for obj in Slideshow.objects.exclude(Q(img_old="") | Q(img_old=None)):
        # Create Photograph instance with StdImage variations from image file
        filename = path.basename(obj.img_old.path)
        file = obj.img_old.open()

        instance = Photograph()
        instance.img.save(filename, file, save=False)
        variations = {
            "large": {
                "width": 1200,
                "height": None,
                "crop": False,
                "resample": 1,
                "kwargs": {},
                "name": "large",
            },
            "medium": {
                "width": 900,
                "height": None,
                "crop": False,
                "resample": 1,
                "kwargs": {},
                "name": "medium",
            },
            "small": {
                "width": 600,
                "height": None,
                "crop": False,
                "resample": 1,
                "kwargs": {},
                "name": "small",
            },
            "thumbnail": {
                "width": 100,
                "height": 100,
                "crop": True,
                "resample": 1,
                "kwargs": {},
                "name": "thumbnail",
            },
        }
        for _, variation in variations.items():
            JPEGFieldFile.render_variation(instance.img.name, variation)
        instance.img_alt = obj.img_alt
        instance.save()

        # Assign created Photograph instance to img field and delete image file
        obj.img = instance
        obj.img_old.delete(save=True)


class Migration(migrations.Migration):

    dependencies = [
        ("photograph", "0005_implement_deep_zoom_fields"),
        ("slideshow", "0005_add_img_fields_slideshow_model"),
    ]

    operations = [
        migrations.RenameField(
            model_name="slideshow", old_name="img", new_name="img_old",
        ),
        migrations.AddField(
            model_name="slideshow",
            name="img",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="photograph.Photograph",
            ),
        ),
        migrations.RunPython(change_img_field, migrations.RunPython.noop),
        migrations.RemoveField(model_name="slideshow", name="img_alt",),
        migrations.RemoveField(model_name="slideshow", name="img_old",),
    ]
