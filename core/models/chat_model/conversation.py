from __future__ import unicode_literals
from django.db import models
from django.utils import timezone


class Conversation(models.Model):
    members = models.ManyToManyField('Person')
    kelaas = models.ForeignKey('Kelaas', related_name="conversations", on_delete=models.CASCADE)
    last_message_time = models.DateTimeField('post creation date', default=timezone.now)

    @property
    def message_count(self):
        return self.messages.count()

    @property
    def member_count(self):
        return self.members.count()

    def __unicode__(self):
        return "id=" + str(self.id) + " members_count =" + str(self.member_count)