# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-10 20:08
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion
import managing_files.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Files',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_valid_1', models.BooleanField(default=True)),
                ('file_name_1', models.CharField(max_length=300)),
                ('path_name_1', models.FileField(upload_to=managing_files.models.user_directory_path)),
                ('is_valid_2', models.BooleanField(default=True)),
                ('file_name_2', models.CharField(max_length=300)),
                ('path_name_2', models.FileField(upload_to=managing_files.models.user_directory_path)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='uploaded date')),
                ('is_finished', models.BooleanField(default=False)),
                ('create_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-creation_date'],
            },
        ),
        migrations.CreateModel(
            name='Reference',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='New reference', max_length=200)),
                ('scentific_name', models.CharField(max_length=200)),
                ('is_obsolete', models.BooleanField(default=False)),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='uploaded date')),
                ('file_name', models.CharField(max_length=300)),
                ('reference', models.FileField(upload_to=managing_files.models.reference_directory_path)),
            ],
            options={
                'ordering': ['-creation_date'],
            },
        ),
        migrations.CreateModel(
            name='Sample',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('date_sample', models.DateField(default='New sample', verbose_name='sample date')),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='uploaded date')),
                ('is_rejected', models.BooleanField(default=False)),
                ('geo_local', django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326)),
                ('files', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sample', to='managing_files.Files')),
                ('user_uploaded', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sample', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-creation_date'],
            },
        ),
        migrations.CreateModel(
            name='Software',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('path_to_run', models.CharField(max_length=300)),
            ],
            options={
                'ordering': ['name', 'version__name'],
            },
        ),
        migrations.CreateModel(
            name='Version',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='software',
            name='version',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='software', to='managing_files.Version'),
        ),
        migrations.AddField(
            model_name='project',
            name='samples',
            field=models.ManyToManyField(related_name='project', to='managing_files.Sample'),
        ),
    ]