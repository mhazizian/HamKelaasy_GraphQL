# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datetime import datetime
import pytz

def pretty_date(diff):
    """
    Get a datetime object or a int() Epoch timestamp and return a
    pretty string like 'an hour ago', 'Yesterday', '3 months ago',
    'just now', etc
    """
    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return ''

    if day_diff == 0:
        if second_diff < 10:
            return "همین الان"
        if second_diff < 60:
            return str(second_diff) + " ثانیه پیش"
        if second_diff < 120:
            return "یک دقیقه پیش"
        if second_diff < 3600:
            return str(second_diff / 60) + " دقیقه پیش"
        if second_diff < 7200:
            return "یک ساعت پیش"
        if second_diff < 86400:
            return str(second_diff / 3600) + " ساعت پیش"
    if day_diff == 1:
        return "دیروز"
    if day_diff < 7:
        return str(day_diff) + " روز پیش"
    if day_diff < 31:
        return str(day_diff / 7) + " هفته پیش"
    if day_diff < 365:
        return str(day_diff / 30) + " ماه پیش"
    return str(day_diff / 365) + " سال پیش"


class Comment(models.Model):
    body = models.CharField('comment body', max_length=1000)
    create_date = models.DateTimeField('post creation date', default=datetime.now)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)

    s_owner = models.ForeignKey('Student', on_delete=models.CASCADE, default=None, null=True)
    t_owner = models.ForeignKey('Teacher', on_delete=models.CASCADE, default=None, null=True)

    @property
    def shamsi_date(self):
        tz = pytz.timezone('Asia/Tehran')
        delta = datetime.now(tz) - self.create_date
        return pretty_date(delta)

    @property
    def owner(self):
        if self.s_owner:
            return self.s_owner
        return self.t_owner

    def __unicode__(self):
        return unicode(self.body)
