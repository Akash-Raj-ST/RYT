# Generated by Django 3.2 on 2022-06-21 12:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Accounts',
            fields=[
                ('user_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=25)),
                ('username', models.CharField(max_length=25, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.TextField(max_length=250)),
                ('dp', models.ImageField(default=None, upload_to='user_dp')),
                ('verified', models.BooleanField(default=False)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('last_login', models.DateTimeField(auto_now=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Places',
            fields=[
                ('p_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('place_name', models.CharField(max_length=50)),
                ('link', models.CharField(max_length=250)),
                ('image', models.ImageField(upload_to='place')),
                ('subject', models.CharField(max_length=100)),
                ('description', models.TextField(max_length=400)),
                ('place_type', models.CharField(choices=[('Country', 'Country'), ('State', 'State'), ('District', 'District'), ('Islands', 'Islands'), ('Beach', 'Beach'), ('Beach resorts', 'Beach resorts'), ('Secluded beaches', 'Secluded beaches'), ('Mountain', 'Mountain'), ('Forest', 'Forest'), ('Dessert', 'Dessert'), ('Countryside', 'Countryside'), ('Town', 'Town'), ('City', 'City'), ('Winter sport', 'Winter sport'), ('Culture and Heritage', 'Culture and Heritage'), ('Religious', 'Religious'), ('Museum', 'Museum'), ('Educational', 'Educational')], max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('r_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('content', models.TextField(max_length=1500)),
                ('likes', models.IntegerField(default=0)),
                ('date_uploaded', models.DateField(default=django.utils.timezone.now)),
                ('p_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.places')),
                ('u_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Review_tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tags', models.CharField(max_length=20)),
                ('r_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.review', verbose_name='r_id_FK')),
            ],
        ),
        migrations.CreateModel(
            name='Review_pic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('r_pic', models.ImageField(upload_to='review')),
                ('r_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.review', verbose_name='r_id_FK')),
            ],
        ),
        migrations.CreateModel(
            name='Review_like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('r_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.review', verbose_name='r_id_FK')),
                ('u_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='u_id_FK')),
            ],
        ),
        migrations.CreateModel(
            name='Place_map',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pm_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='api.places', verbose_name='M1_place')),
                ('spm_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.places', verbose_name='S1_place')),
            ],
        ),
    ]