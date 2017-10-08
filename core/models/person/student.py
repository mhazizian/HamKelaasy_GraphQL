from __future__ import unicode_literals

import random

from django.utils.crypto import get_random_string

from core.models.person import Person
from django.db import models
from core import HamkelaasyError, Error_code

STUDENT_KEY_WORD = "student"


class Student(Person):
    age = models.IntegerField('student age')
    code = models.CharField('invite link for parent', max_length=10)
    gender = models.IntegerField('gender type(1 for men, 0 for women)', default=None, null=True, blank=True)

    parents = models.ForeignKey('Parent', related_name="childes", on_delete=models.SET_NULL, null=True, default=None)

    class Meta:
        ordering = ['-id']

    def save(self, *args, **kwargs):
        if not self.pk:
            self.code = Student.generate_code()
            if not self.profile_pic:
                self.profile_pic.name = 'student/people' + str(random.randint(1, 11)) + '.png'
        if self.gender != 0 and self.gender != 1:
            raise HamkelaasyError(Error_code.Student.Bad_gender)
        if self.age > 18 or self.age < 6:
            raise HamkelaasyError(Error_code.Student.Bad_age)

        self.type = STUDENT_KEY_WORD
        super(Student, self).save(args, kwargs)

    def __unicode__(self):
        return "student: " + unicode(self.last_name)

    @staticmethod
    def generate_code():
        code = get_random_string(length=5, allowed_chars='123456789QWERTYUIOPASDFGHJKLZXCVBNM')

        while Student.objects.filter(code=code).exists():
            code = get_random_string(length=5, allowed_chars='123456789QWERTYUIOPASDFGHJKLZXCVBNM')
        return code
