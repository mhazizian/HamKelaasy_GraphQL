from __future__ import unicode_literals

import os
from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string
from uuid import uuid4

from Hamkelaasy_graphQL import settings


def get_uuid():
    file_uuid = str(uuid4())
    return file_uuid


def get_upload_path(instance, filename):
    return '/'.join(['data', get_random_string(length=32), filename])


class File(models.Model):
    title = models.CharField('file title', max_length=200)
    description = models.CharField('file body', max_length=1000, blank=True, default='')
    create_date = models.DateTimeField('file creation date', default=timezone.now)
    owner = models.ForeignKey('Person', related_name="uploaded_files", on_delete=models.CASCADE)

    uuid = models.CharField('uuid', unique=True, max_length=36, default=get_uuid)

    data = models.FileField('file', upload_to=get_upload_path)

    def delete(self, *args, **kwargs):
        os.remove(os.path.join(settings.MEDIA_ROOT, self.data.name))
        super(File, self).delete(*args, **kwargs)

    @property
    def url(self):
        return settings.SERVER_ADDR[:-1] + self.data.url

    def __unicode__(self):
        return unicode(self.title)

    @staticmethod
    def create(input_file, owner, title="", description=""):
        f = File(
            title=title if title is not "" else input_file.name,
            description=description,
            data=input_file,
            owner=owner,
        )
        f.save()
        return f


class Sys_file(models.Model):
    title = models.CharField('file title', max_length=200)
    data = models.FileField('file', upload_to='sys/')
    '''
    registered titles:
    
    >certificate : pic for each certificate model pic
    >certificate <level num> : pic for all certificates_level with same level_num 
    '''

    def delete(self, *args, **kwargs):
        os.remove(os.path.join(settings.MEDIA_ROOT, self.data.name))
        super(Sys_file, self).delete(*args, **kwargs)

    def __unicode__(self):
        return unicode(self.title)
