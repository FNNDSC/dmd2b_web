# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-10 15:19
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0013_auto_20160810_1443'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studydetails',
            name='StudyID',
        ),
    ]
