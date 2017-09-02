# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datetime import datetime
import pytz
from core.models.utilz import pretty_date


class Comment(models.Model):
    body = models.CharField('comment body', max_length=1000)
    create_date = models.DateTimeField('post creation date', default=datetime.now)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)

    owner = models.ForeignKey('Person', on_delete=models.CASCADE)

    @property
    def time_passed(self):
        tz = pytz.timezone('Asia/Tehran')
        delta = datetime.now(tz) - self.create_date
        return pretty_date(delta)

    def __unicode__(self):
        return unicode(self.body)
