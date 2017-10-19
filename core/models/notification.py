# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from enum import Enum

from core.utilz import pretty_past_time, to_shamsi_date


class Notification_type(object):
    class Teacher(Enum):
        new_student = 1001
        new_message = 1002  # also will have conversation id
        new_comment = 1003  # also will have post id
        student_added_parent = 1004  # also will have student id

    class Parent(Enum):
        new_message = 2001  # also will have conversation id
        new_story = 2002  # also will have kelaas id
        new_comment = 2003  # also will have post id
        child_joined_kelaas = 2004  # also will have child id

    class Student(Enum):
        new_post = 3001  # also will have post id
        new_kelaas_joined = 3002  # also will have kelaas id
        new_badge = 3003  # will also have badge id


class Notification(models.Model):
    receiver = models.ForeignKey('Person', related_name='notifications')
    has_seen = models.BooleanField(default=False)

    create_date = models.DateTimeField('notification creation date', default=timezone.now)

    type_code = models.IntegerField('notification type code')
    related_id = models.IntegerField('id of releated object')

    # type_id = models.IntegerField

    class Meta:
        ordering = ('-id',)

    @property
    def shamsi_date(self):
        return to_shamsi_date(self.create_date)

    @property
    def time_passed(self):
        delta = timezone.now() - self.create_date
        return pretty_past_time(delta)
