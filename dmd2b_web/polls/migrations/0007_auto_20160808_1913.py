# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-08 19:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0006_auto_20160808_1856'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientdetails',
            name='PatientID',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='studydetails',
            name='StudyID',
            field=models.CharField(max_length=100),
        ),
    ]
