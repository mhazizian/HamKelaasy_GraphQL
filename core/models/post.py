# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datetime import datetime
import pytz

from core.models.utilz import pretty_date
from khayyam import *


class Post(models.Model):
    title = models.CharField('post title', max_length=200, null=True)
    description = models.CharField('post body', max_length=1000)
    create_date = models.DateTimeField('post creation date', default=datetime.now)
    type = models.CharField('post type', max_length=7, default='')

    kelaas = models.ForeignKey('Kelaas', on_delete=models.CASCADE)

    @property
    def shamsi_date(self):
        local_tz = pytz.timezone('Asia/Tehran')
        return JalaliDatetime(self.create_date.replace(tzinfo=pytz.utc).astimezone(local_tz)).strftime(
            '%A %D %B %N  %h:%v')

    @property
    def time_passed(self):
        tz = pytz.timezone('Asia/Tehran')
        delta = datetime.now(tz) - self.create_date
        return pretty_date(delta)

    def __unicode__(self):
        return unicode(self.title)


class Kelaas_post(Post):
    files = models.ManyToManyField('File', blank=True)

    def save(self, *args, **kwargs):
        self.type = 'Kelaas_post'
        super(Kelaas_post, self).save(args, kwargs)


class Story(Post):
    story_pic = models.FileField('story pic', upload_to='story/%Y/%m/%d/', blank=True)

    @property
    def pic(self):
        return self.story_pic.url

    def save(self, *args, **kwargs):
        self.type = 'Story'
        super(Story, self).save(args, kwargs)
