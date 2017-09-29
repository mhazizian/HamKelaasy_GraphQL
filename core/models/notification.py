# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from core.models.utilz import pretty_past_time
from khayyam import JalaliDatetime

NOTIFICATION_KEY_WORD = 'Notification'


class System_notification(models.Model):
    reciver = models.ForeignKey('Person', related_name='notifications')
    has_seen = models.BooleanField(default=False)

    title = models.CharField('notification title', max_length=200)
    message = models.CharField('notification body', max_length=1000)
    create_date = models.DateTimeField('notification creation date', default=timezone.now)

    type = models.CharField('notification type', max_length=30)
    # type_id = models.IntegerField

    class Meta:
        ordering = ('-id', )

    def save(self, *args, **kwargs):
        self.type = NOTIFICATION_KEY_WORD
        super(System_notification, self).save(args, kwargs)

    @property
    def shamsi_date(self):
        return JalaliDatetime(self.create_date).strftime(
            '%A %D %B %N  %h:%v')

    @property
    def time_passed(self):
        delta = timezone.now() - self.create_date
        return pretty_past_time(delta)
