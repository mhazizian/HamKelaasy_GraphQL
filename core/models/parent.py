from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from .person import Person

PARENT_KEY_WORD = "parent"


class Parent(Person):
    def save(self, *args, **kwargs):
        self.type = PARENT_KEY_WORD
        super(Parent, self).save(args, kwargs)

    def __unicode__(self):
        return "parents: " + unicode(self.last_name)
