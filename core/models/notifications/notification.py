# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from core.utilz import pretty_past_time, to_shamsi_date


class Notification(models.Model):
    receiver = models.ForeignKey('Person', related_name='notifications')
    has_seen = models.BooleanField(default=False)

    create_date = models.DateTimeField('notification creation date', default=timezone.now)

    type_code = models.IntegerField('notification type code')
    related_ids = models.CharField('ids of related object, seperated by ","', max_length=100)
    related_text = models.CharField('related text for notification', max_length=500)

    class Meta:
        ordering = ('-id',)

    @property
    def shamsi_date(self):
        return to_shamsi_date(self.create_date)

    @property
    def time_passed(self):
        delta = timezone.now() - self.create_date
        return pretty_past_time(delta)
