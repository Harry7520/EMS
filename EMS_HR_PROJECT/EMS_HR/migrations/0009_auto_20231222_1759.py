# Generated by Django 2.2 on 2023-12-22 11:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('EMS_HR', '0008_updatemodel_proj'),
    ]

    operations = [
        migrations.RenameField(
            model_name='updatemodel',
            old_name='proj',
            new_name='post',
        ),
    ]
