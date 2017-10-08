from __future__ import unicode_literals

from .person import Person
from django.db import models
from core import HamkelaasyError, Error_code

TEACHER_KEY_WORD = "teacher"


class Teacher(Person):
    gender = models.IntegerField('gender type(1 for men, 0 for women)', default=None, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.type = TEACHER_KEY_WORD
        if not self.profile_pic:
            self.profile_pic.name = 'teacher.svg'
        if self.gender != 0 and self.gender != 1:
            raise HamkelaasyError(Error_code.Teacher.Bad_gender)
        super(Teacher, self).save(args, kwargs)

    def __unicode__(self):
        return "teacher: " + unicode(self.last_name)
