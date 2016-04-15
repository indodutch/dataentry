# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-13 12:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Drive',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(help_text="Label added to the drive, e.g., 'kumbhmela_5'.", max_length=50)),
                ('external', models.BooleanField(default=False, help_text='True when the drive is external and false otherwise.')),
                ('time_added', models.DateTimeField(blank=True, help_text='Time when the drive was added to the drive bay.', null=True)),
                ('time_removed', models.DateTimeField(blank=True, help_text='Time when the drive was removed from the drive bay.', null=True)),
                ('whereabouts', models.TextField(blank=True, help_text='Whereabouts of this drive copy, e.g., who had it lasts, where is it now etc. (optional).', max_length=1000)),
                ('note', models.TextField(blank=True, help_text='Additional notes on this (collection of) drive(s) (optional).', max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='DriveCopy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(help_text="Label added to the drive, e.g., 'kumbhmela_5II'.", max_length=50)),
                ('number', models.IntegerField(help_text='Drive copy number.')),
                ('whereabouts', models.TextField(blank=True, help_text='Whereabouts of this drive copy, e.g., who had it lasts, where is it now etc. (optional).', max_length=1000)),
                ('note', models.TextField(blank=True, help_text='Additional notes on this drive copy (optional).', max_length=1000)),
                ('drive', models.ForeignKey(help_text='The unique drive it is a copy of.', on_delete=django.db.models.deletion.CASCADE, to='dataentry.Drive')),
            ],
        ),
        migrations.CreateModel(
            name='Experiment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name of the subexperiment.', max_length=100)),
                ('number', models.IntegerField(help_text='Number of the subexperiment.')),
                ('description', models.TextField(blank=True, help_text='Short description of the experiment (optional).', max_length=1000)),
                ('note', models.TextField(blank=True, help_text='Additional notes on the subexperiment (optional).', max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_added', models.DateTimeField(auto_now=True, help_text='Time when the drive was added to the drive bay (optional).')),
                ('size', models.IntegerField(blank=True, help_text='Size in bytes (optional).', null=True)),
                ('start_recording', models.DateTimeField(blank=True, help_text='Time when the recording started (optional).', null=True)),
                ('end_recording', models.DateTimeField(blank=True, help_text='Time when the recording ended (optional).', null=True)),
                ('note', models.TextField(blank=True, help_text='Additional notes on this file (optional).', max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Format',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('extension', models.CharField(help_text="Extension of the file (in small letters!), e.g., '.txt' and not '.TXT'.", max_length=50)),
                ('description', models.TextField(blank=True, help_text='Description of the file format (optional).', max_length=10000)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.FloatField(blank=True, help_text='Optional.')),
                ('longitude', models.FloatField(blank=True, help_text='Optional.')),
                ('description', models.TextField(blank=True, help_text='Description of the location (optional).', max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='First and last name.', max_length=100)),
                ('email', models.CharField(blank=True, help_text='Email address(es) (optional).', max_length=200)),
                ('note', models.TextField(blank=True, help_text='Notes (optional).', max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Sensor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sensor_type', models.CharField(help_text="Short description of the sensor, e.g., 'GoPro Camera'.", max_length=100)),
                ('note', models.TextField(blank=True, help_text='Notes for this sensor (optional).', max_length=1000)),
                ('format', models.ManyToManyField(blank=True, help_text='The format for the output of this sensor (optional).', to='dataentry.Format')),
                ('location', models.ManyToManyField(blank=True, help_text='The location for this sensor (optional).', to='dataentry.Location')),
            ],
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text="Name of the data source (e.g., 'Local Police')", max_length=200)),
                ('note', models.TextField(blank=True, help_text='Additional notes on this data source (optional).', max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='StorageLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(help_text='Path of the file on the drive.', max_length=300)),
                ('drive', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dataentry.Drive')),
                ('file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dataentry.File')),
            ],
        ),
        migrations.AddField(
            model_name='file',
            name='drive',
            field=models.ManyToManyField(help_text='The drives on which the file is stored.', through='dataentry.StorageLocation', to='dataentry.Drive'),
        ),
        migrations.AddField(
            model_name='file',
            name='experiment',
            field=models.ManyToManyField(blank=True, help_text='The subexperiment this file belongs to (optional).', to='dataentry.Experiment'),
        ),
        migrations.AddField(
            model_name='file',
            name='format',
            field=models.ForeignKey(blank=True, help_text='Format of the file (optional).', null=True, on_delete=django.db.models.deletion.CASCADE, to='dataentry.Format'),
        ),
        migrations.AddField(
            model_name='file',
            name='location',
            field=models.ForeignKey(blank=True, help_text='Location where the recording took place (optional).', null=True, on_delete=django.db.models.deletion.CASCADE, to='dataentry.Location'),
        ),
        migrations.AddField(
            model_name='file',
            name='sensor',
            field=models.ForeignKey(blank=True, help_text='Sensor used to obtain the data (optional).', null=True, on_delete=django.db.models.deletion.CASCADE, to='dataentry.Sensor'),
        ),
        migrations.AddField(
            model_name='file',
            name='source',
            field=models.ForeignKey(blank=True, help_text='The data source (optional).', null=True, on_delete=django.db.models.deletion.CASCADE, to='dataentry.Source'),
        ),
        migrations.AddField(
            model_name='experiment',
            name='contactperson',
            field=models.ForeignKey(help_text='Main contact person for this subexperiment.', on_delete=django.db.models.deletion.CASCADE, to='dataentry.Person'),
        ),
    ]