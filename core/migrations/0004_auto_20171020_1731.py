# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-20 14:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_notification'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='related_id',
        ),
        migrations.AddField(
            model_name='notification',
            name='related_ids',
            field=models.CharField(default='', max_length=100, verbose_name='ids of related object, seperated by ","'),
            preserve_default=False,
        ),
    ]
