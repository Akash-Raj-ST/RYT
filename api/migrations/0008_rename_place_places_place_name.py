# Generated by Django 3.2 on 2021-09-19 04:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20210918_1455'),
    ]

    operations = [
        migrations.RenameField(
            model_name='places',
            old_name='place',
            new_name='place_name',
        ),
    ]
