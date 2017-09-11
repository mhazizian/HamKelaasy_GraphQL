from __future__ import unicode_literals

from django.utils import timezone
from django.db import models

from Hamkelaasy_graphQL import settings
from core.models import Sys_file
from core.models.utilz import pretty_date
from khayyam import JalaliDatetime


class Certificate(models.Model):
    title = models.CharField('certificate title', max_length=200)
    description = models.CharField('certificate desc', max_length=400)
    create_date = models.DateTimeField('post creation date', default=timezone.now)

    creator = models.ForeignKey('Person', related_name="created_certificates",on_delete=models.CASCADE)

    @property
    def pic(self):
        f = Sys_file.objects.get(title="certificate")
        return settings.SERVER_ADDR[:-1] + f.data.url

    @property
    def time_passed(self):
        delta = timezone.now() - self.create_date
        return pretty_date(delta)

    @property
    def shamsi_date(self):
        return JalaliDatetime(self.create_date).strftime(
            '%A %D %B %N  %h:%v')

    def __unicode__(self):
        return self.title


class Certificate_level(models.Model):
    type = models.ForeignKey(Certificate, related_name="levels", on_delete=models.CASCADE)

    level = models.IntegerField('certificate-level', default=1)
    level_description = models.CharField('description for level', max_length=500)
    create_date = models.DateTimeField('post creation date', default=timezone.now)

    @property
    def pic(self):
        f = Sys_file.objects.get(title="certificate " + str(self.level))
        return settings.SERVER_ADDR[:-1] + f.data.url

    @property
    def time_passed(self):
        delta = timezone.now() - self.create_date
        return pretty_date(delta)

    @property
    def shamsi_date(self):
        return JalaliDatetime(self.create_date).strftime(
            '%A %D %B %N  %h:%v')

    def __unicode__(self):
        return self.type.title + " level: " + str(self.level)


class Certificate_link(models.Model):
    certificate_level = models.ForeignKey('Certificate_level', related_name="links", on_delete=models.CASCADE)
    assigner = models.ForeignKey('Person', related_name='aasigned_certificate', on_delete=models.CASCADE)
    owner = models.ForeignKey('Person', related_name='certificates', on_delete=models.CASCADE)

    create_date = models.DateTimeField('class creation date', default=timezone.now)

    @property
    def time_passed(self):
        delta = timezone.now() - self.create_date
        return pretty_date(delta)

    @property
    def shamsi_date(self):
        return JalaliDatetime(self.create_date).strftime(
            '%A %D %B %N  %h:%v')
