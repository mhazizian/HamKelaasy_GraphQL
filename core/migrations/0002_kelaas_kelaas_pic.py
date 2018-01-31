# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-16 03:15
from __future__ import unicode_literals

import core.models.kelaas
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='kelaas',
            name='kelaas_pic',
            field=models.FileField(default=None, null=True, upload_to=core.models.kelaas.get_upload_path, verbose_name='kelaas pic'),
        ),
    ]
