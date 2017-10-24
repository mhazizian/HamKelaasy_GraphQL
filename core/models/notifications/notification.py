# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from core.utilz import pretty_past_time, to_shamsi_date
from .notification_doc import Notification_type


class Notification(models.Model):
    receiver = models.ForeignKey('Person', related_name='notifications')
    has_seen = models.BooleanField(default=False)

    create_date = models.DateTimeField('notification creation date', default=timezone.now)

    type_code = models.IntegerField('notification type code')
    related_ids = models.CharField('ids of related object, seperated by ","', max_length=100)
    related_text = models.CharField('related text for notification', max_length=500)

    class Meta:
        ordering = ('-id',)

    @property
    def shamsi_date(self):
        return to_shamsi_date(self.create_date)

    @property
    def time_passed(self):
        delta = timezone.now() - self.create_date
        return pretty_past_time(delta)

    # ****************************************************************************************
    # ****************************************************************************************

    @staticmethod
    def create_new_message(reciver, message, kelaas):
        notif = Notification(
            receiver=reciver,
            type_code=Notification_type.General.new_message.value,
            related_ids=str(message.conversation.id) + ',' + str(kelaas.id) + ',' + str(message.id),
            related_text=message.body
        )
        notif.save()
        return notif

    @staticmethod
    def create_teacher__new_student(teacher, student, kelaas):
        notif = Notification(
            receiver=teacher,
            type_code=Notification_type.Teacher.new_student.value,
            related_ids=str(kelaas.id) + ',' + str(student.id),
            related_text=student.first_name + ',' + student.last_name
        )
        notif.save()
        return notif

    @staticmethod
    def create_teacher__new_parent(teacher, student, kelaas):
        notif = Notification(
            receiver=teacher,
            type_code=Notification_type.Teacher.new_parent.value,
            related_ids=str(kelaas.id) + ',' + str(student.id) + ',' + str(student.parents.id),
            related_text=student.first_name + ',' + student.last_name
        )
        notif.save()
        return notif

    @staticmethod
    def create_teacher__new_comment(teacher, comment, kelaas):
        notif = Notification(
            receiver=teacher,
            type_code=Notification_type.Teacher.new_comment.value,
            related_ids=str(comment.post.id) + ',' + str(kelaas.id) + ',' + str(comment.owner.id),
            related_text=comment.owner.first_name + ',' + comment.owner.last_name + ',' + comment.body
        )
        notif.save()
        return notif

