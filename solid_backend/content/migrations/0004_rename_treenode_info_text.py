# Generated by Django 3.0.9 on 2021-02-09 12:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0003_rename_treenode_node_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='treenode',
            old_name='info_text',
            new_name='info',
        ),
    ]
