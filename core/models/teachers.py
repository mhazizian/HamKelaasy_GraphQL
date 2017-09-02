from __future__ import unicode_literals

from django.contrib.auth.models import User

from .person import Person
from django.db import models


class Teacher(Person):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    kelasses = models.ManyToManyField('Kelaas', blank=True)

    type = models.CharField('user type', max_length=7, default='teacher')

    def __unicode__(self):
        return "teacher: " + unicode(self.last_name)
