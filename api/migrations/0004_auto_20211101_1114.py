# Generated by Django 3.2 on 2021-11-01 05:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20211018_0923'),
    ]

    operations = [
        migrations.AlterField(
            model_name='places',
            name='place_type',
            field=models.CharField(choices=[('Country', 'Country'), ('State', 'State'), ('District', 'District'), ('Islands', 'Islands'), ('Beach resorts', 'Beach resorts'), ('Secluded beaches', 'Secluded beaches'), ('Mountain', 'Mountain'), ('Forest', 'Forest'), ('Dessert', 'Dessert'), ('Countryside', 'Countryside'), ('Town', 'Town'), ('City', 'City'), ('Winter sport', 'Winter sport'), ('Culture and Heritage', 'Culture and Heritage'), ('Religious', 'Religious')], max_length=20),
        ),
        migrations.AlterField(
            model_name='review',
            name='content',
            field=models.TextField(max_length=400),
        ),
    ]
