from __future__ import unicode_literals

from django.db import models


class User_temp(models.Model):
    fard_access_token = models.CharField('temp for saving access token', max_length=100)
    username = models.CharField('temp for user', max_length=100)

    first_name = models.CharField('first name', max_length=200, null=True, blank=True)
    last_name = models.CharField('last name', max_length=200, null=True, blank=True)
    email = models.CharField('email address', max_length=200, null=True, blank=True)
    gender = models.IntegerField('gender type(1 for men, 0 for women)', default=None, null=True, blank=True)
