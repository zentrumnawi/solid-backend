# Generated by Django 3.0.9 on 2021-02-09 13:26

import django.db.models.deletion
import mptt.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("content", "0005_alter_treenode_name_attributes"),
        ("sample_content", "0006_alter_sampleprofile_systematics"),
    ]

    operations = [
        migrations.AddField(
            model_name="sampleprofile",
            name="tree_node",
            field=mptt.fields.TreeForeignKey(
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="profiles",
                related_query_name="profile",
                to="content.TreeNode",
            ),
        ),
    ]
