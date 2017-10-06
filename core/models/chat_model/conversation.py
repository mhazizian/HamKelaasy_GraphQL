from __future__ import unicode_literals
from django.db import models
from django.utils import timezone

DIALOG_KEY_WORD = "dialog"
GROUP_KEY_WORD = "group"


class Conversation(models.Model):
    members = models.ManyToManyField('Person', related_name="conversations")
    kelaas = models.ForeignKey('Kelaas', related_name="conversations", on_delete=models.CASCADE)

    last_message_time = models.DateTimeField('post creation date', default=timezone.now)
    type = models.CharField('conversation type', max_length=10, default='')

    @property
    def message_count(self):
        return self.messages.count()

    @property
    def member_count(self):
        return self.members.count()

    def __unicode__(self):
        return "id=" + str(self.id)


class Conversation_dialog(Conversation):
    def save(self, *args, **kwargs):
        if self.pk:
            if not self.members.count() == 2:
                raise Exception('invalid member count')
        self.type = DIALOG_KEY_WORD
        super(Conversation_dialog, self).save(args, kwargs)

    def has_same_users(self, user1, user2):
        try:
            if self.members.all()[0].id == user1.id and self.members.all()[1].id == user2.id:
                return True

            if self.members.all()[1].id == user1.id and self.members.all()[0].id == user2.id:
                return True
        except IndexError:
            return False

        return False


class Conversation_group(Conversation):
    def save(self, *args, **kwargs):
        self.type = GROUP_KEY_WORD
        super(Conversation_group, self).save(args, kwargs)
