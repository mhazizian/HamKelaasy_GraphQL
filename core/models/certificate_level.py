from __future__ import unicode_literals

from django.utils import timezone
from django.db import models
from core.models import Sys_file


class Certificate(models.Model):
    title = models.CharField('certificate title', max_length=200)
    description = models.CharField('certificate desc', max_length=400)

    creator = models.ForeignKey('Person', on_delete=models.CASCADE)

    @property
    def pic(self):
        f = Sys_file.objects.get(title="certificate")
        return f.data.url

    def __unicode__(self):
        return self.title


class Certificate_level(models.Model):
    type = models.ForeignKey(Certificate, on_delete=models.CASCADE)

    level = models.IntegerField('certificate-level', default=1)
    level_description = models.CharField('description for level', max_length=500)

    @property
    def pic(self):
        f = Sys_file.objects.get(title="certificate " + str(self.level))
        return f.data.url

    def __unicode__(self):
        return self.type.title + " level: " + str(self.level)


class Certificate_link(models.Model):
    certificate_level = models.ForeignKey('Certificate_level', on_delete=models.CASCADE)
    assigner = models.ForeignKey('Person', related_name='certificate_assigner', on_delete=models.CASCADE)
    student = models.ForeignKey('Student', related_name='related_to_student', on_delete=models.CASCADE)

    create_date = models.DateTimeField('class creation date', default=timezone.now)
