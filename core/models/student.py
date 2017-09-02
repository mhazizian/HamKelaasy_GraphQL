from __future__ import unicode_literals

from django.contrib.auth.models import User

from .person import Person
from django.db import models


class Student(Person):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField('student age', default=None, null=True)
    nickname = models.CharField('nick name', max_length=50, null=True)

    certificates = models.ManyToManyField('Certificate', blank=True)  # each student has many certificates
    parents = models.ForeignKey('Parent', on_delete=models.CASCADE, null=True, default=None)

    parent_code = models.CharField('invite link for parent', max_length=10)

    type = models.CharField('user type', max_length=7, default='student')

    def __unicode__(self):
        return "student: " + unicode(self.last_name)