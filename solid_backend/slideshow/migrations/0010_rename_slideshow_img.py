# Generated by Django 3.0.9 on 2021-02-20 23:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("slideshow", "0009_remove_default_from_position_fields"),
    ]

    operations = [
        migrations.RenameField(
            model_name="slideshow", old_name="img", new_name="title_image",
        ),
    ]