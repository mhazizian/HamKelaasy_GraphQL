from __future__ import unicode_literals

import uuid

from .person import Person
from django.db import models

STUDENT_KEY_WORD = "student"


class Student(Person):
    age = models.IntegerField('student age', default=None, null=True)
    nickname = models.CharField('nick name', max_length=50, null=True)

    parent_code = models.CharField('invite link for parent', max_length=10)

    certificates = models.ManyToManyField('Certificate', blank=True)  # each student has many certificates
    parents = models.ForeignKey('Parent', on_delete=models.CASCADE, null=True, default=None, blank=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            parent_code = str(uuid.uuid4())[:5].upper()

            while Student.objects.filter(parent_code=parent_code).exists():
                parent_code = str(uuid.uuid4())[:5].upper()
            self.parent_code = parent_code
        self.type = STUDENT_KEY_WORD
        super(Student, self).save(args, kwargs)

    def __unicode__(self):
        return "student: " + unicode(self.last_name)
