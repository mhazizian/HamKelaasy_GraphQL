# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-19 16:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_kelaas_kelaas_pic'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('has_seen', models.BooleanField(default=False)),
                ('create_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='notification creation date')),
                ('type_code', models.IntegerField(verbose_name='notification type code')),
                ('related_id', models.IntegerField(verbose_name='id of related object')),
                ('related_text', models.CharField(max_length=500, verbose_name='related text for notification')),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='core.Person')),
            ],
            options={
                'ordering': ('-id',),
            },
        ),
    ]
