# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-01 19:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdditionalHeaderInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fov', models.CharField(max_length=200)),
                ('dimensions', models.CharField(max_length=200)),
                ('VoxelSizes', models.CharField(max_length=200)),
                ('PrimarySliceDirection', models.CharField(max_length=200)),
                ('ProtocolName', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='PatientDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('PatientID', models.IntegerField(default=0)),
                ('PatientSex', models.CharField(max_length=100)),
                ('PatientBirthDate', models.DateTimeField(verbose_name='date of birth')),
                ('Age_Days', models.IntegerField(default=0)),
                ('PatientName', models.CharField(max_length=100)),
                ('PatientReportedAge', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='SeriesDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('SeriesID', models.CharField(max_length=200)),
                ('SeriesDescription', models.CharField(max_length=200)),
                ('Modality', models.CharField(max_length=100)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.PatientDetails')),
            ],
        ),
        migrations.CreateModel(
            name='StudyDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('StudyID', models.IntegerField(default=0)),
                ('StudyDescription', models.CharField(max_length=100)),
                ('StudyDate', models.DateTimeField(verbose_name='date published')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.PatientDetails')),
            ],
        ),
        migrations.AddField(
            model_name='seriesdetails',
            name='study',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.StudyDetails'),
        ),
        migrations.AddField(
            model_name='additionalheaderinfo',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.PatientDetails'),
        ),
        migrations.AddField(
            model_name='additionalheaderinfo',
            name='series',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.SeriesDetails'),
        ),
    ]
