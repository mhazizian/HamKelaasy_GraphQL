from __future__ import unicode_literals
from django.db import models


class Conversation(models.Model):
    members = models.ManyToManyField('Person')
    kelaas = models.ForeignKey('Kelaas', related_name="conversations", on_delete=models.CASCADE)

    @property
    def message_count(self):
        return self.messages.count()
