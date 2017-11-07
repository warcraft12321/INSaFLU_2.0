# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-07 11:17
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import fluwebvirus.formatChecker
import managing_files.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('managing_files', '0013_auto_20171105_1224'),
    ]

    operations = [
        migrations.CreateModel(
            name='SeasonReference',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='season_reference', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='UploadFiles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_valid', models.BooleanField(default=False)),
                ('file_name', models.CharField(blank=True, max_length=300, null=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='uploaded date')),
                ('path_name', fluwebvirus.formatChecker.ContentTypeRestrictedFileField(blank=True, null=True, upload_to=managing_files.models.user_directory_path)),
                ('is_day_month_year_from_date_of_onset', models.BooleanField(default=False)),
                ('is_day_month_year_from_date_of_collection', models.BooleanField(default=False)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='upload_files', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['creation_date'],
            },
        ),
        migrations.CreateModel(
            name='VacineStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vacine_status', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.RemoveField(
            model_name='reference',
            name='scientific_name',
        ),
        migrations.RemoveField(
            model_name='sample',
            name='sample_date',
        ),
        migrations.AddField(
            model_name='reference',
            name='description',
            field=models.CharField(blank=True, default='', max_length=500, null=True, verbose_name='Description'),
        ),
        migrations.AddField(
            model_name='reference',
            name='isolate_name',
            field=models.CharField(default='', max_length=200, verbose_name='Isolate Name'),
        ),
        migrations.AddField(
            model_name='sample',
            name='date_of_collection',
            field=models.DateField(blank=True, null=True, verbose_name='date of collection'),
        ),
        migrations.AddField(
            model_name='sample',
            name='date_of_onset',
            field=models.DateField(blank=True, null=True, verbose_name='date of onset'),
        ),
        migrations.AddField(
            model_name='sample',
            name='date_of_receipt_lab',
            field=models.DateField(blank=True, null=True, verbose_name='date of receipt lab'),
        ),
        migrations.AddField(
            model_name='sample',
            name='day',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sample',
            name='has_files',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='sample',
            name='month',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sample',
            name='week',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sample',
            name='year',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='tagname',
            name='is_meta_data',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='reference',
            name='number_of_locus',
            field=models.IntegerField(default=0, verbose_name='#Sequences'),
        ),
        migrations.AlterField(
            model_name='sample',
            name='is_valid_1',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='sample',
            name='is_valid_2',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='sample',
            name='path_name_1',
            field=fluwebvirus.formatChecker.ContentTypeRestrictedFileField(blank=True, null=True, upload_to=managing_files.models.user_directory_path),
        ),
        migrations.AlterField(
            model_name='sample',
            name='path_name_2',
            field=fluwebvirus.formatChecker.ContentTypeRestrictedFileField(blank=True, null=True, upload_to=managing_files.models.user_directory_path),
        ),
        migrations.AddField(
            model_name='reference',
            name='season',
            field=models.ManyToManyField(to='managing_files.SeasonReference'),
        ),
        migrations.AddField(
            model_name='sample',
            name='vaccine_status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sample', to='managing_files.VacineStatus'),
        ),
    ]
