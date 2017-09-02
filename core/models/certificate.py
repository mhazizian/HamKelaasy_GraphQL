from __future__ import unicode_literals

from django.db import models
from core.models import Sys_file


class Certificate_type(models.Model):
    title = models.CharField('certificate tile', max_length=200)
    description = models.CharField('certificate desc', max_length=400)

    granter = models.ForeignKey('Teacher', on_delete=models.CASCADE)

    @property
    def url(self):
        f = Sys_file.objects.get(title="certificate")
        return f.data.url

    def __unicode__(self):
        return self.title


class Certificate(models.Model):
    type = models.ForeignKey(Certificate_type, on_delete=models.CASCADE)

    level = models.IntegerField('certificate-level', default=1)
    level_description = models.CharField('description for level', max_length=500)

    @property
    def url(self):
        f = Sys_file.objects.get(title="certificate " + str(self.level))
        return f.data.url

    def __unicode__(self):
        return self.type.title + " level: " + str(self.level)
