# Generated by Django 3.0.9 on 2021-09-20 15:06

from django.db import migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        ('slideshow', '0011_rename_slideshowimage_img'),
    ]

    operations = [
        migrations.AddField(
            model_name='slideshow',
            name='categories',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
