# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-09 16:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('managing_files', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dataset',
            options={'ordering': ['creation_date', 'name']},
        ),
        migrations.AlterModelOptions(
            name='vacinestatus',
            options={'ordering': ['creation_date', 'name']},
        ),
        migrations.AlterField(
            model_name='reference',
            name='name',
            field=models.CharField(db_index=True, max_length=200, verbose_name='New reference'),
        ),
    ]
