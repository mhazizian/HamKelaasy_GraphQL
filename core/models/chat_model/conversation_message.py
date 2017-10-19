from __future__ import unicode_literals
from django.db import models
from django.utils import timezone

from core.utilz import pretty_past_time
from core.utilz import to_shamsi_date


class Conversation_message(models.Model):
    writer = models.ForeignKey('Person', on_delete=models.CASCADE)
    conversation = models.ForeignKey('Conversation', related_name="messages", on_delete=models.CASCADE)

    body = models.CharField('message body', max_length=1000)
    create_date = models.DateTimeField('message creation date', default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.conversation.last_message_time = timezone.now()
            self.conversation.save()
        super(Conversation_message, self).save(args, kwargs)

    def __unicode__(self):
        return self.writer.first_name + " body:" + self.body

    @property
    def time_passed(self):
        delta = timezone.now() - self.create_date
        return pretty_past_time(delta)

    @property
    def shamsi_date(self):
        return to_shamsi_date(self.create_date)


