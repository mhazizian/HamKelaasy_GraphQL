from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

from core import HamkelaasyError
from .person import Person

PARENT_KEY_WORD = "parent"


class Parent(Person):
    def my_save(self):
        self.type = PARENT_KEY_WORD
        if not self.profile_pic:
            self.profile_pic.name = 'parent.svg'
        self.save()

    def __unicode__(self):
        return unicode(self.id) + unicode(self.first_name) + " " + unicode(self.last_name) + "parent"
