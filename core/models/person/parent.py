from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

from core import myGraphQLError
from .person import Person

PARENT_KEY_WORD = "parent"


class Parent(Person):
    def save(self, *args, **kwargs):
        self.type = PARENT_KEY_WORD
        if not self.profile_pic:
            self.profile_pic.name = 'parent.svg'
        super(Parent, self).save(args, kwargs)

    def __unicode__(self):
        return "parents: " + unicode(self.last_name)

    def get_childes(self, user):
        if not self.id == user.id:
            raise myGraphQLError('Permission denied', status=403)

        return self.childes.all()

    def get_child(self, user, childe_id):
        if not self.id == user.id:
            raise myGraphQLError('Permission denied', status=403)

        try:
            return self.childes.get(pk=childe_id)
        except Parent.DoesNotExist:
            raise myGraphQLError('Child not found', status=404)
