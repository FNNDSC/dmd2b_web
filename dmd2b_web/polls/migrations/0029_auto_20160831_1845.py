# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-31 18:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0028_auto_20160831_1844'),
    ]

    operations = [
        migrations.AlterField(
            model_name='additionalheaderinfo',
            name='ProtocolName',
            field=models.CharField(max_length=100),
        ),
    ]