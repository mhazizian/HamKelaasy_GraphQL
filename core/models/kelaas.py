from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string

from Hamkelaasy_graphQL import settings
from core.utilz import to_shamsi_date


def get_upload_path(instance, filename):
    return '/'.join(['profile_pic', get_random_string(length=32), filename])


class Kelaas(models.Model):
    title = models.CharField('class name', max_length=200)
    create_date = models.DateTimeField('class creation date', default=timezone.now)
    description = models.CharField('class description', max_length=500)
    gender = models.IntegerField('gender type(1 for men, 0 for women, 2 for both)')
    kelaas_pic = models.FileField('kelaas pic', upload_to=get_upload_path, default=None, null=True)

    tags = models.ManyToManyField('Tag', related_name="kelaases", blank=True)
    students = models.ManyToManyField('Student', related_name="kelaases", blank=True)
    teacher = models.ForeignKey('Teacher', related_name='kelaases')

    invite_code = models.CharField('invite link for kelaas', max_length=10)
    is_public = models.BooleanField(default=False)

    @property
    def shamsi_date(self):
        return to_shamsi_date(self.create_date)

    @property
    def pic(self):
        return settings.SERVER_ADDR[:-1] + self.kelaas_pic.url

    def save(self, *args, **kwargs):
        if not self.pk:
            self.invite_code = Kelaas.generate_invite_code()
        if not self.kelaas_pic:
            self.kelaas_pic.name = 'kelaas/default.svg'
        super(Kelaas, self).save(args, kwargs)

    def __unicode__(self):
        return self.title

    @staticmethod
    def generate_invite_code():
        invite_code = get_random_string(length=5, allowed_chars='123456789QWERTYUIOPASDFGHJKLZXCVBNM')

        while Kelaas.objects.filter(invite_code=invite_code).exists():
            invite_code = get_random_string(length=5, allowed_chars='123456789QWERTYUIOPASDFGHJKLZXCVBNM')
        return invite_code
