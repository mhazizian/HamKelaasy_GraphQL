from __future__ import unicode_literals

from django.db import models
from django.utils.crypto import get_random_string

from Hamkelaasy_graphQL import settings


def get_upload_path(instance, filename):
    return '/'.join(['badges', get_random_string(length=32), filename])


class Badge(models.Model):
    title = models.CharField('badge names', max_length=200)
    badge_pic = models.FileField('badge pic', upload_to=get_upload_path, null=True)

    class Meta:
        ordering = ['-id']

    def __unicode__(self):
        return self.title

    @property
    def pic(self):
        return settings.SERVER_ADDR[:-1] + self.badge_pic.url


class Badge_link(models.Model):
    type = models.ForeignKey(Badge, related_name="links", on_delete=models.CASCADE)
    kelaas = models.ForeignKey('Kelaas', related_name="badges", on_delete=models.CASCADE)
    count = models.IntegerField('number of achiving this badge', default=1)

    student = models.ForeignKey('Student', related_name="badges", on_delete=models.CASCADE)

    class Meta:
        ordering = ['-id']

    @property
    def pic(self):
        return settings.SERVER_ADDR[:-1] + self.type.badge_pic.url

    @property
    def title(self):
        return self.type.title
