# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-03 12:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataentry', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='related_file',
            field=models.ManyToManyField(blank=True, help_text='Other related files.', null=True, related_name='_file_related_file_+', to='dataentry.File'),
        ),
    ]
