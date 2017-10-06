from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string

from khayyam import *


class Kelaas(models.Model):
    title = models.CharField('class name', max_length=200)
    create_date = models.DateTimeField('class creation date', default=timezone.now)
    description = models.CharField('class description', max_length=500)
    genedr = models.IntegerField('gender type(1 for men, 0 for women, 2 for both)', default=1)

    tags = models.ManyToManyField('Tag', related_name="kelaases", blank=True)
    students = models.ManyToManyField('Student', related_name="kelaases", blank=True)
    teacher = models.ForeignKey('Teacher', related_name='kelaases')

    invite_code = models.CharField('invite link for kelaas', max_length=10)
    is_public = models.BooleanField(default=False)

    @property
    def shamsi_date(self):
        return JalaliDatetime(self.create_date).strftime(
            '%A %D %B %N  %h:%v')

    def save(self, *args, **kwargs):
        if not self.pk:
            self.invite_code = Kelaas.generate_invite_code()
        super(Kelaas, self).save(args, kwargs)

    def __unicode__(self):
        return self.title

    @staticmethod
    def generate_invite_code():
        invite_code = get_random_string(length=5, allowed_chars='123456789QWERTYUIOPASDFGHJKLZXCVBNM')

        while Kelaas.objects.filter(invite_code=invite_code).exists():
            invite_code = get_random_string(length=5, allowed_chars='123456789QWERTYUIOPASDFGHJKLZXCVBNM')
        return invite_code
