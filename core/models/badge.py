from __future__ import unicode_literals

from django.db import models


class Badge(models.Model):
    title = models.CharField('badge names', max_length=200)
    pic = models.FileField('badge pic', upload_to='badges/', null=True)

    def __unicode__(self):
        return self.title


class Badge_link(models.Model):
    type = models.ForeignKey(Badge, related_name="links", on_delete=models.CASCADE)
    kelaas = models.ForeignKey('Kelaas', related_name="badges", on_delete=models.CASCADE)
    count = models.IntegerField('number of achiving this badge', default=1)

    student = models.ForeignKey('Student',related_name="badges" , on_delete=models.CASCADE)

    @property
    def pic(self):
        return self.badge.type.pic.url

    @property
    def title(self):
        return self.type.title
