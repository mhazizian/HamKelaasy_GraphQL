from __future__ import unicode_literals

from django.db import models


class Badge_type(models.Model):
    title = models.CharField('badge names', max_length=200)
    pic = models.FileField('badge pic', upload_to='badges/', null=True)

    def __unicode__(self):
        return self.title


class Badge(models.Model):
    type = models.ForeignKey(Badge_type, on_delete=models.CASCADE)
    kelaas = models.ForeignKey('Kelaas', on_delete=models.CASCADE)
    students = models.ManyToManyField('Student', blank=True)

    def __unicode__(self):
        return "badge : " + self.type.title + " for Kelaas : " + self.kelaas.title
