from __future__ import unicode_literals

from core import myGraphQLError
from .person import Person
from django.db import models

TEACHER_KEY_WORD = "teacher"


class Teacher(Person):
    kelaases = models.ManyToManyField('Kelaas', related_name="teachers", blank=True)

    def save(self, *args, **kwargs):
        self.type = TEACHER_KEY_WORD
        if not self.profile_pic:
            self.profile_pic.name = 'teacher.svg'
        super(Teacher, self).save(args, kwargs)

    def __unicode__(self):
        return "teacher: " + unicode(self.last_name)

    def get_kelaases(self, user):
        if not user.id == self.id:
            raise myGraphQLError('Permission denied', status=403)

        return self.kelaases.all().order_by('-id')

    def get_kelaas(self, user, kelaas_id):
        if not user.id == self.id:
            raise myGraphQLError('Permission denied', status=403)

        try:
            return self.kelaases.get(pk=kelaas_id)
        except:
            raise myGraphQLError('Kelaas not found', status=404)
