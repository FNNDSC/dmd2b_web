# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-11 15:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0019_auto_20160811_1526'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientdetails',
            name='Age_Days',
            field=models.CharField(max_length=25),
        ),
        migrations.AlterField(
            model_name='patientdetails',
            name='PatientBirthDate',
            field=models.CharField(max_length=25),
        ),
        migrations.AlterField(
            model_name='patientdetails',
            name='PatientID',
            field=models.CharField(max_length=25),
        ),
        migrations.AlterField(
            model_name='patientdetails',
            name='PatientName',
            field=models.CharField(max_length=25),
        ),
        migrations.AlterField(
            model_name='patientdetails',
            name='PatientReportedAge',
            field=models.CharField(max_length=25),
        ),
        migrations.AlterField(
            model_name='patientdetails',
            name='PatientSex',
            field=models.CharField(max_length=25),
        ),
        migrations.AlterField(
            model_name='seriesdetails',
            name='Modality',
            field=models.CharField(max_length=25),
        ),
        migrations.AlterField(
            model_name='studydetails',
            name='StudyDate',
            field=models.CharField(max_length=25),
        ),
        migrations.AlterField(
            model_name='studydetails',
            name='StudyID',
            field=models.CharField(max_length=25),
        ),
    ]