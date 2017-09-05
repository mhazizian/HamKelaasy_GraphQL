# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.sessions.models import Session
from core.models import Student, Kelaas, Parent, Post, Tag, Teacher, Certificate, Badge_type,\
    Badge, Person, File, Certificate_type, Sys_file, Story, Comment, Kelaas_post, Certificate_link, User_temp

# Register your models here.

admin.site.register(Session)

admin.site.register(Person)
admin.site.register(Kelaas)
admin.site.register(Student)
admin.site.register(Parent)
admin.site.register(Teacher)
admin.site.register(Tag)
admin.site.register(Post)
admin.site.register(Certificate)
admin.site.register(Badge)
admin.site.register(Badge_type)
admin.site.register(File)
admin.site.register(Certificate_type)
admin.site.register(Sys_file)
admin.site.register(Story)
admin.site.register(Comment)
admin.site.register(Kelaas_post)
admin.site.register(Certificate_link)
admin.site.register(User_temp)