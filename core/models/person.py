from __future__ import unicode_literals
from django.db import models


class Person(models.Model):
    first_name = models.CharField('first name', max_length=200, null=True, blank=True)
    last_name = models.CharField('last name', max_length=200, null=True, blank=True)
    email = models.CharField('email address', max_length=200, null=True, blank=True)
    gender = models.IntegerField('gender type(1 for men, 0 for women)', default=None, null=True, blank=True)

    access_token = models.CharField('access_token for getting data from fard.ir', max_length=100)
    signup_completed = models.BooleanField('define whether the signup progress completed or not', default=False)

    profile_pic = models.FileField('profile pic', upload_to="profile_pic/", blank=True)

    @property
    def pic(self):
        return self.profile_pic.url

    def __unicode__(self):
        return unicode(self.first_name) + " " + unicode(self.last_name) + " username: "