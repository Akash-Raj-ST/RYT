# Generated by Django 3.2 on 2022-07-11 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review_pic',
            name='r_pic',
            field=models.FileField(upload_to=''),
        ),
    ]
