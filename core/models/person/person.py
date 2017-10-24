from __future__ import unicode_literals

import json

from django.db import models
from django.contrib.auth.models import User

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.crypto import get_random_string
from rest_framework.authtoken.models import Token

from core.utilz import hash_password


def get_upload_path(instance, filename):
    return '/'.join(['profile_pic', get_random_string(length=32), filename])


class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    password = models.CharField('password', max_length=128, default=None, null=True)
    has_new_password = models.BooleanField('is on new hashing algorithm or not', default=False)

    type = models.CharField('user type', max_length=7, default='')

    first_name = models.CharField('first name', max_length=200, null=True, blank=True)
    last_name = models.CharField('last name', max_length=200, null=True, blank=True)
    email = models.CharField('email address', max_length=200, null=True, default=None)

    phone_number = models.CharField('phone number', max_length=12, default='')
    phone_number_verified = models.BooleanField('determine whether phone is verified or not', default=False)

    create_date = models.DateTimeField('creation date')
    profile_pic = models.FileField('profile pic', upload_to=get_upload_path, blank=True)

    signup_completed = models.BooleanField('signup progress completed(bool)', default=False)
    last_sys_notification_seen = models.DateTimeField('last_sys_notification_seen', default=None, null=True)

    fard_access_token = models.CharField('access_token for getting data from fard.ir', max_length=100, default='')

    @property
    def pic(self):
        return settings.SERVER_ADDR[:-1] + self.profile_pic.url

    def save(self, *args, **kwargs):
        if not self.pk:
            self.create_date = timezone.now()
            if self.password:
                self.password = hash_password(self.create_date, self.password)
                self.has_new_password = True
        super(Person, self).save(args, kwargs)

    def __unicode__(self):
        return ('id:' + str(self.id) + ' username:' + (self.user.username if self.user else "None")
                + ' firstName:' + self.first_name + ' lastName:' + self.last_name + ' type:' + self.type
                + ' hasNewPass:' + str(self.has_new_password) + ' phone:' + self.phone_number)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
