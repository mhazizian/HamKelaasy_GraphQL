from __future__ import unicode_literals

import random
import uuid

from django.utils.crypto import get_random_string

from core.models.person import Person
from django.db import models

STUDENT_KEY_WORD = "student"


class Student(Person):
    age = models.IntegerField('student age', default=None, null=True)
    # nickname = models.CharField('nick name', max_length=50, null=True)
    parent_code = models.CharField('invite link for parent', max_length=10)

    parents = models.ForeignKey('Parent', related_name="childes", on_delete=models.SET_NULL, null=True, default=None)

    class Meta:
        ordering = ['-id']

    def save(self, *args, **kwargs):
        if not self.pk:
            self.parent_code = Student.generate_parent_code()
            if not self.profile_pic:
                self.profile_pic.name = 'student/people' + str(random.randint(1, 13)) + '.png'

        self.type = STUDENT_KEY_WORD
        super(Student, self).save(args, kwargs)

    def __unicode__(self):
        return "student: " + unicode(self.last_name)

    @staticmethod
    def generate_parent_code():
        parent_code = get_random_string(length=5, allowed_chars='123456789QWERTYUIOPASDFGHJKLZXCVBNM')

        while Student.objects.filter(parent_code=parent_code).exists():
            parent_code = get_random_string(length=5, allowed_chars='123456789QWERTYUIOPASDFGHJKLZXCVBNM')
        return parent_code
