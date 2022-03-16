# Generated by Django 3.0.9 on 2022-02-01 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("glossary", "0004_remove_img_fields"),
    ]

    operations = [
        migrations.AlterField(
            model_name="glossaryentry",
            name="links",
            field=models.ManyToManyField(
                blank=True, null=True, to="glossary.GlossaryEntry"
            ),
        ),
        migrations.AlterField(
            model_name="glossaryentry",
            name="text",
            field=models.TextField(
                blank=True, null=True, verbose_name="text (Markdown)"
            ),
        ),
    ]
