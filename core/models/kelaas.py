from __future__ import unicode_literals

import uuid

from django.db import models
from django.utils import timezone
from khayyam import *
import pytz


class Kelaas(models.Model):
    title = models.CharField('class name', max_length=200)
    create_date = models.DateTimeField('class creation date', default=timezone.now)
    description = models.CharField('class description', max_length=500)

    tags = models.ManyToManyField('Tag', related_name="kelaases", blank=True)
    students = models.ManyToManyField('Student', related_name="kelaases", blank=True)

    invite_code = models.CharField('invite link for kelaas', max_length=10)

    @property
    def shamsi_date(self):
        local_tz = pytz.timezone('Asia/Tehran')
        return JalaliDatetime(self.create_date.replace(tzinfo=pytz.utc).astimezone(local_tz)).strftime(
            '%A %D %B %N  %h:%v')

    def save(self, *args, **kwargs):
        if not self.pk:
            self.invite_code = Kelaas.generate_invite_code()
        super(Kelaas, self).save(args, kwargs)

    def __unicode__(self):
        return self.title

    @staticmethod
    def generate_invite_code():
        invite_code = str(uuid.uuid4())[:7].upper()

        while Kelaas.objects.filter(invite_code=invite_code).exists():
            invite_code = str(uuid.uuid4())[:7].upper()
        return invite_code
