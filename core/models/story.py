# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datetime import datetime
import pytz
from khayyam import *


class Story(models.Model):
    description = models.CharField('post body', max_length=1000)
    create_date = models.DateTimeField('post creation date', default=datetime.now)
    kelaas = models.ForeignKey('Kelaas', on_delete=models.CASCADE)  # each post is related to a specific kelaas

    story_pic = models.FileField('story pic', upload_to='story/%Y/%m/%d/', blank=True)

    @property
    def shamsi_date(self):
        local_tz = pytz.timezone('Asia/Tehran')
        return JalaliDatetime(self.create_date.replace(tzinfo=pytz.utc).astimezone(local_tz)).strftime(
            '%A %D %B %N  %h:%v')

    @property
    def pic(self):
        return self.profile_pic.url

    def __unicode__(self):
        return unicode(self.title)
