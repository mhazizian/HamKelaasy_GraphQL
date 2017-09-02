# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datetime import datetime
import pytz
from khayyam import *

class Post(models.Model):
    title = models.CharField('post title', max_length=200)
    description = models.CharField('post body', max_length=1000)
    create_date = models.DateTimeField('post creation date', default=datetime.now)
    kelaas = models.ForeignKey('Kelaas', on_delete=models.CASCADE)  # each post is related to a specific kelaas

    files = models.ManyToManyField('File', blank=True)

    @property
    def shamsi_date(self):
        local_tz = pytz.timezone('Asia/Tehran')
        return JalaliDatetime(self.create_date.replace(tzinfo=pytz.utc).astimezone(local_tz)).strftime('%A %D %B %N  %h:%v')

    def __unicode__(self):
        return unicode(self.title)
