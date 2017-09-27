from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.crypto import get_random_string
from rest_framework.authtoken.models import Token


def get_upload_path(instance, filename):
    return '/'.join(['profile_pic', get_random_string(length=32), filename])


class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    first_name = models.CharField('first name', max_length=200, null=True, blank=True)
    last_name = models.CharField('last name', max_length=200, null=True, blank=True)
    email = models.CharField('email address', max_length=200, null=True, blank=True)
    gender = models.IntegerField('gender type(1 for men, 0 for women)', default=None, null=True, blank=True)
    profile_pic = models.FileField('profile pic', upload_to=get_upload_path, blank=True)

    fard_access_token = models.CharField('access_token for getting data from fard.ir', max_length=100)

    signup_completed = models.BooleanField('signup progress completed(bool)', default=False)
    type = models.CharField('user type', max_length=7, default='')
    last_sys_notofication_seen = models.DateTimeField('class creation date', default=None, null=True)

    @property
    def pic(self):
        return settings.SERVER_ADDR[:-1] + self.profile_pic.url

    def __unicode__(self):
        return unicode(self.first_name) + " " + unicode(self.last_name) + " username: "


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
