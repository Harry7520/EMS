# Generated by Django 2.2 on 2023-12-21 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EMS_HR', '0003_auto_20231217_1800'),
    ]

    operations = [
        migrations.AddField(
            model_name='leavemodel',
            name='status',
            field=models.CharField(default='pending', max_length=12),
        ),
        migrations.AddField(
            model_name='resmodel',
            name='status',
            field=models.CharField(default='pending', max_length=12),
        ),
    ]
