from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from .person import Person


class Parent(Person):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    type = models.CharField('user type', max_length=7, default='parent')

    def __unicode__(self):
        return "parents: " + unicode(self.last_name)