# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-01-31 08:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_file_uuid'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='link',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]
