# Generated by Django 3.0.9 on 2022-03-15 16:18

from django.db import migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        ('quiz', '0008_quizquestion_new_tags'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quizquestion',
            name='tags',
        ),
        migrations.RenameField(
            model_name='quizquestion',
            old_name='new_tags',
            new_name="tags"
        ),
    ]
