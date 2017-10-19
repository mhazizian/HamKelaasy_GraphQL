# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from core.models.utilz import pretty_past_time, to_shamsi_date



class Comment(models.Model):
    body = models.CharField('comment body', max_length=1000)
    create_date = models.DateTimeField('post creation date', default=timezone.now)
    post = models.ForeignKey('Post', related_name="comments", on_delete=models.CASCADE)

    owner = models.ForeignKey('Person', related_name="comments", on_delete=models.CASCADE)

    @property
    def time_passed(self):
        delta = timezone.now() - self.create_date
        return pretty_past_time(delta)

    @property
    def shamsi_date(self):
        return to_shamsi_date(self.create_date)

    def __unicode__(self):
        return unicode(self.body)
