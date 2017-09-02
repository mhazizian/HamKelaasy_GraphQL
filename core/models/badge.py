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

    def __unicode__(self):
        return "badge : " + self.type.title + " for Kelaas : " + self.kelaas.title


class Badge_link(models.Model):
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    count = models.IntegerField('number of achiving this badge', default=0)

    student = models.ForeignKey('Student', on_delete=models.CASCADE)
