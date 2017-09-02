from __future__ import unicode_literals

from django.db import models
from datetime import datetime
# from khayyam import *
import pytz


class File(models.Model):
    title = models.CharField('file title', max_length=200)
    description = models.CharField('file body', max_length=1000, blank=True)
    create_date = models.DateTimeField('file creation date', default=datetime.now)
    owner = models.ForeignKey('Person', on_delete=models.CASCADE)

    data = models.FileField('file', upload_to='%Y/%m/%d/')


class Sys_file(models.Model):
    title = models.CharField('file title', max_length=200)
    data = models.FileField('file', upload_to='sys/')

    def __unicode__(self):
        return unicode(self.title)