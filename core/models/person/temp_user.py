from __future__ import unicode_literals

from django.db import models


class User_temp(models.Model):
    fard_access_token = models.CharField('temp for saving access token', max_length=100)
    username = models.CharField('temp for user', max_length=100)
