from __future__ import unicode_literals

from django.contrib.auth.models import User

from .person import Person
from django.db import models

TEACHER_KEY_WORD = "teacher"


class Teacher(Person):
    kelasses = models.ManyToManyField('Kelaas', blank=True)

    def save(self, *args, **kwargs):
        self.type = TEACHER_KEY_WORD
        super(Teacher, self).save(args, kwargs)

    def __unicode__(self):
        return "teacher: " + unicode(self.last_name)
