from __future__ import unicode_literals

import uuid

from django.db import models
from datetime import datetime
from khayyam import *
import pytz


class Kelaas(models.Model):
    title = models.CharField('class name', max_length=200)
    create_date = models.DateTimeField('class creation date', default=datetime.now)
    description = models.CharField('class description', max_length=500)
    students = models.ManyToManyField('Student', blank=True)  # each Kelaas has  many students
    tags = models.ManyToManyField('Tag', blank=True)  # each Kelaas has many tags

    invite_code = models.CharField('invite link for kelaas', max_length=10)

    @property
    def shamsi_date(self):
        local_tz = pytz.timezone('Asia/Tehran')
        return JalaliDatetime(self.create_date.replace(tzinfo=pytz.utc).astimezone(local_tz)).strftime(
            '%A %D %B %N  %h:%v')

    def save(self, *args, **kwargs):
        if not self.pk:
            invite_code = str(uuid.uuid4())[:5].upper()

            while Kelaas.objects.filter(invite_code=invite_code).exists():
                invite_code = str(uuid.uuid4())[:5].upper()
            self.invite_code = invite_code

        super(Kelaas, self).save(args, kwargs)

    def __unicode__(self):
        return self.title
