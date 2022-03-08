# Generated by Django 3.0.9 on 2022-03-08 16:44

from django.db import migrations, models
from solid_backend.media_object.models import MediaObjectField

def migrate_Photograph_to_MediaObject(apps, schema_editor):
    ContentType = apps.get_model('contenttypes', 'ContentType')
    QuizQuestion = apps.get_model("quiz", "QuizQuestion")
    MediaObject = apps.get_model("media_object", "MediaObject")
    quiz_content_type = ContentType.objects.get_for_model(QuizQuestion)

    for q in QuizQuestion.objects.all():
        for img in q.img.all():
            _file = img.img.file
            # get the original file name without path remnants
            _file.name = _file.name.split("/")[-1]
            audio_file = None
            if img.audio:
                audio_file = img.audio
                audio_file.name = audio_file.name.split("/")[-1]
            _dzi_file = None
            if img.dzi_option:
                _dzi_file = img.dzi_file

            m = MediaObject.objects.create(
                object_id=q.id,
                content_type=quiz_content_type,
                media_format="image",
                file=_file,
                dzi_option=img.dzi_option,
                dzi_file=_dzi_file,
                img_original_width=img.img_original_width,
                img_original_height=img.img_original_height,
                img_original_scale=img.img_original_scale,
                img_alt=img.img_alt,
                description=img.description,
                audio=audio_file,
                date=img.date,
                author=img.author,
                license=img.license,
            )
            m.file.field = MediaObjectField(variations={
            "large": (1200, None),
            "medium": (900, None),
            "small": (600, None),
            "thumbnail": (100, 100, True)})
            m.file.render_variations()
            img.delete()


def migrate_MediaObject_to_Photograph(apps, schema_editor):
    QuizQuestion = apps.get_model("quiz", "QuizQuestion")
    Photograph = apps.get_model("photograph", "Photograph")
    MediaObject = apps.get_model("media_object", "MediaObject")
    ContentType = apps.get_model('contenttypes', 'ContentType')
    quiz_content_type = ContentType.objects.get_for_model(QuizQuestion)

    for q in QuizQuestion.objects.all():
        for media_obj in MediaObject.objects.filter(content_type__pk=quiz_content_type.pk, object_id=q.id):
            _file = media_obj.file.file
            # get the original file name without path remnants
            _file.name = _file.name.split("/")[-1]
            audio_file = None
            if media_obj.audio:
                audio_file = media_obj.audio
                audio_file.name = audio_file.name.split("/")[-1]

            p = Photograph.objects.create(
                profile_position=media_obj.profile_position,
                img=_file,
                img_original_width=media_obj.img_original_width,
                img_original_height=media_obj.img_original_height,
                img_original_scale=media_obj.img_original_scale,
                img_alt=media_obj.img_alt,
                description=media_obj.description,
                audio=audio_file,
                date=media_obj.date,
                author=media_obj.author,
                license=media_obj.license,
            )
            q.img.add(p)
            media_obj.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0005_auto_20220222_1829'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quizquestion',
            name='type',
            field=models.CharField(choices=[('SC', 'Single Choice'), ('MC', 'Multiple Choice'), ('DD', 'Drag and Drop'), ('TF', 'True or False'), ('RN', 'Range'), ('RG', 'Ranking'), ('HS', 'Hotspot')], max_length=2),
        ),
        migrations.RunPython(migrate_Photograph_to_MediaObject, migrate_MediaObject_to_Photograph)
    ]