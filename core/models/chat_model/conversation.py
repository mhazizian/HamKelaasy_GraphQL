from __future__ import unicode_literals
from django.db import models


class Conversation(models.Model):
    members = models.ManyToManyField('Person')

    @staticmethod
    def make_converstaion_id(list_of_members_id):
        nums = list_of_members_id[:]
        nums.sort()

        return nums