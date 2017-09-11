from __future__ import unicode_literals
from django.db import models


class Conversation_message(models.Model):
    writer = models.ForeignKey('Person', on_delete=models.CASCADE)
    body = models.CharField('message body', max_length=1000)
    conversation = models.ForeignKey('Conversation', related_name="messages", on_delete=models.CASCADE)

    def __unicode__(self):
        return self.writer.first_name + " body:" + self.body


