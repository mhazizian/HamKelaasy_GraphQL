from __future__ import unicode_literals

from .person import Person
from django.db import models
from core import HamkelaasyError, Error_code

TEACHER_KEY_WORD = "teacher"


class Teacher(Person):
    gender = models.IntegerField('gender type(1 for men, 0 for women)', default=None, null=True, blank=True)

    def my_save(self):
        self.type = TEACHER_KEY_WORD
        if not self.profile_pic:
            self.profile_pic.name = 'teacher.svg'
        if self.gender != 0 and self.gender != 1:
            raise HamkelaasyError(Error_code.Teacher.Bad_gender)
        self.save()

    def __unicode__(self):
        return unicode(self.id) + unicode(self.first_name) + " " + unicode(self.last_name) + "teacher"
