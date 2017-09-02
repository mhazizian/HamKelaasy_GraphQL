from __future__ import unicode_literals

from django.db import models
from datetime import datetime
# from khayyam import *
import pytz


class File(models.Model):
    title = models.CharField('file title', max_length=200)
    description = models.CharField('file body', max_length=1000, blank=True)
    create_date = models.DateTimeField('file creation date', default=datetime.now)
    data = models.FileField('file', upload_to='%Y/%m/%d/')

    # @property
    # def shamsi_date(self):
    #     local_tz = pytz.timezone('Asia/Tehran')
    #     return JalaliDatetime(self.create_date.replace(tzinfo=pytz.utc).astimezone(local_tz)).strftime('%A %D %B %N  %h:%v')
    #
    # def __unicode__(self):
    #     return unicode(self.title)


class Sys_file(models.Model):
    title = models.CharField('file title', max_length=200)
    data = models.FileField('file', upload_to='sys/')

    def __unicode__(self):
        return unicode(self.title)