# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-01-30 12:50
from __future__ import unicode_literals

import core.models.files_link
from django.db import migrations, models
from uuid import uuid4

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_post_seen'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='uuid',
            field=models.CharField(default=uuid4, max_length=36, unique=False, verbose_name='uuid'),
            ),
    ]