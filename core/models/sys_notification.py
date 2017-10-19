# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from core.models.utilz import pretty_past_time, to_shamsi_date

SYSTEM_NOTIFICATION_KEY_WORD = 'System_notification'


class System_notification(models.Model):
    title = models.CharField('post title', max_length=200)
    description = models.CharField('post body', max_length=1000)
    create_date = models.DateTimeField('sys_notification creation date', default=timezone.now)
    type = models.CharField('notification type', max_length=30)

    class Meta:
        ordering = ('-id', )

    def save(self, *args, **kwargs):
        self.type = SYSTEM_NOTIFICATION_KEY_WORD
        super(System_notification, self).save(args, kwargs)

    @property
    def shamsi_date(self):
        return to_shamsi_date(self.create_date)

    @property
    def time_passed(self):
        delta = timezone.now() - self.create_date
        return pretty_past_time(delta)
