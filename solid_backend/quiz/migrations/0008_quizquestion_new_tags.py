# Generated by Django 3.0.9 on 2022-03-15 16:05

from django.db import migrations
import taggit.managers

from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


def old_to_new_tags(apps, schema_editor):
    QuizQuestion = apps.get_model("quiz", "QuizQuestion")
    Tag = apps.get_model("taggit", "Tag")
    TaggedItem = apps.get_model("taggit", "TaggedItem")
    ContentType = apps.get_model('contenttypes', 'ContentType')
    ct = ContentType.objects.get_for_model(QuizQuestion)
    for q in QuizQuestion.objects.all():
        if q.tags:
            for tag in q.tags:
                t, created = Tag.objects.get_or_create(name=tag, slug=tag)
                tagged_items = TaggedItem.objects.get_or_create(
                    content_type_id=ct.id,
                    object_id=q.id,
                    tag=t
                )
            q.tags = []
            q.save()


def new_to_old_tags(apps, schema_editor):
    QuizQuestion = apps.get_model("quiz", "QuizQuestion")
    TaggedItem = apps.get_model("taggit", "TaggedItem")
    ContentType = apps.get_model('contenttypes', 'ContentType')
    ct = ContentType.objects.get_for_model(QuizQuestion)
    for q in QuizQuestion.objects.all():
        tagged_items = TaggedItem.objects.filter(object_id=q.id, content_type_id=ct.id,)
        q.tags = list(map(lambda t: t.tag.name, tagged_items))
        q.save()
        for t in tagged_items:
            t.tag.delete()
        tagged_items.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        ('quiz', '0007_remove_quizquestion_img'),
    ]

    operations = [
        migrations.AddField(
            model_name='quizquestion',
            name='new_tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
        migrations.RunPython(old_to_new_tags, new_to_old_tags),
    ]
