from __future__ import unicode_literals

import json

from django.contrib.auth.models import User
from django.db import models

from core import HamkelaasyError
from .person import Person

PARENT_KEY_WORD = "parent"


class Parent(Person):
    def my_save(self):
        self.type = PARENT_KEY_WORD
        if not self.profile_pic:
            self.profile_pic.name = 'parent.png'
        self.save()

    def __unicode__(self):
        return ('id:' + str(self.id) + ' username:' + (self.user.username if self.user else "None")
                + ' firstName:' + self.first_name + ' lastName:' + self.last_name + ' type:' + self.type
                + ' hasNewPass:' + str(self.has_new_password) + ' phone:' + self.phone_number)
        # return unicode(json.dumps(
        #     {
        #         'id': self.id,
        #         'username': self.user.username,
        #         'firstName': self.first_name,
        #         'lastName': self.last_name,
        #         'type': self.type,
        #         'hasNewPass': self.has_new_password,
        #         'phone': self.phone_number,
        #     })
        # )
