# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-16 07:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('managing_files', '0018_sample_is_ready_for_projects'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectsample',
            name='is_error',
            field=models.BooleanField(default=False),
        ),
    ]