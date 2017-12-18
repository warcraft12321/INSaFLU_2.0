# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-14 14:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('managing_files', '0004_metakeyreference'),
    ]

    operations = [
        migrations.CreateModel(
            name='MixedInfections',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('average_value', models.FloatField(default=0.0)),
                ('description', models.TextField(default='')),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='uploaded date')),
                ('has_master_vector', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['tag'],
            },
        ),
        migrations.CreateModel(
            name='MixedInfectionsTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, db_index=True, max_length=50, null=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='mixedinfections',
            name='tag',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mixed_infections', to='managing_files.MixedInfectionsTag'),
        ),
        migrations.AddField(
            model_name='projectsample',
            name='mixed_infections',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='project_sample', to='managing_files.MixedInfections'),
        ),
    ]