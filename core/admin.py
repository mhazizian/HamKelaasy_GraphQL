# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.sessions.models import Session
from core.models import Student, Kelaas, Parent, Post, Tag, Teacher, Certificate_level, \
    Badge, Person, File, Certificate, Sys_file, Story, Comment, Kelaas_post, Certificate_link, User_temp, Badge_link, \
    Conversation, Conversation_message, Task, Temp_phone_number, Notification

# Register your models here.

admin.site.register(Session)

admin.site.register(Person)
admin.site.register(Kelaas)
admin.site.register(Student)
admin.site.register(Parent)
admin.site.register(Teacher)
admin.site.register(Tag)
admin.site.register(Post)
admin.site.register(Certificate_level)
admin.site.register(Badge)
admin.site.register(Badge_link)
admin.site.register(File)
admin.site.register(Certificate)
admin.site.register(Sys_file)
admin.site.register(Story)
admin.site.register(Comment)
admin.site.register(Kelaas_post)
admin.site.register(Certificate_link)
admin.site.register(User_temp)
admin.site.register(Conversation)
admin.site.register(Conversation_message)
admin.site.register(Task)
admin.site.register(Temp_phone_number)
admin.site.register(Notification)
