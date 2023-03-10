# Generated by Django 2.2.28 on 2023-03-09 16:43

import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import re


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, unique=True)),
                ('mediaCoverImage', models.ImageField(blank=True, upload_to='')),
                ('writer', models.CharField(max_length=50)),
                ('language', models.CharField(max_length=50)),
                ('publishDate', models.DateField(blank=True)),
                ('avgScore', models.FloatField(default=0)),
                ('type', models.CharField(default=None, max_length=50)),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', models.ImageField(blank=True, upload_to='')),
                ('age', models.IntegerField(validators=[django.core.validators.MinValueValidator(13)])),
                ('joinDate', models.DateField(default=datetime.date.today)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('duration', models.DurationField(default=datetime.timedelta(0))),
                ('media', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='shelves_project.Media')),
            ],
        ),
        migrations.CreateModel(
            name='Show',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('episodes', models.IntegerField(default=0)),
                ('seasons', models.IntegerField(default=0)),
                ('media', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='shelves_project.Media')),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=50)),
                ('duration', models.DurationField(default=datetime.timedelta(0))),
                ('media', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='shelves_project.Media')),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isbn', models.CharField(max_length=13, validators=[django.core.validators.MinLengthValidator(13), django.core.validators.RegexValidator(re.compile('^\\d+(?:\\d+)*\\Z'), code='invalid', message=None)])),
                ('media', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='shelves_project.Media')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('rating', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)])),
                ('comment', models.TextField(blank=True, max_length=1000)),
                ('publishDate', models.DateField(default=datetime.date.today)),
                ('likes', models.IntegerField(default=0)),
                ('slug', models.SlugField(unique=True)),
                ('media', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shelves_project.Media')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('media', 'user')},
            },
        ),
    ]
