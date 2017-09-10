from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
# from khayyam import *
import pytz


class File(models.Model):
    title = models.CharField('file title', max_length=200)
    description = models.CharField('file body', max_length=1000, blank=True, default='')
    create_date = models.DateTimeField('file creation date', default=timezone.now)
    owner = models.ForeignKey('Person', related_name="uploaded_files",on_delete=models.CASCADE)

    data = models.FileField('file', upload_to='data/%Y/%m/%d/')

    @property
    def url(self):
        return self.data.url

    def __unicode__(self):
        return unicode(self.title)

class Sys_file(models.Model):
    title = models.CharField('file title', max_length=200)
    data = models.FileField('file', upload_to='sys/')

    def __unicode__(self):
        return unicode(self.title)