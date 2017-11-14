# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import logging

from django.contrib.auth.models import User
from django.shortcuts import render
import core.services as services

from core.models import *
from datetime import datetime
from datetime import timedelta

logger = logging.getLogger('core')


def info(request):
    last_hour = datetime.now() - timedelta(hours=1)
    yesterday = datetime.now() - timedelta(hours=24)
    last_week = datetime.now() - timedelta(days=7)
    last_month = datetime.now() - timedelta(days=30)

    return render(request, 'core/info.html', {
        'user_count': Person.objects.count(),
        'student_count': Student.objects.count(),
        'parent_count': Parent.objects.count(),
        'teacher_count': Teacher.objects.count(),
        'kelaas_count': Kelaas.objects.count(),
        'story_count': Story.objects.count(),
        'kelaas_post_count': Kelaas_post.objects.count(),
        'comment_count': Comment.objects.count(),
        'message_count': Conversation_message.objects.count(),

        'today_user_count': Person.objects.filter(create_date__gte=yesterday).count(),
        'today_parent_count': Parent.objects.filter(create_date__gte=yesterday).count(),
        'today_student_count': Student.objects.filter(create_date__gte=yesterday).count(),
        'today_teacher_count': Teacher.objects.filter(create_date__gte=yesterday).count(),
        'today_kelaas_count': Kelaas.objects.filter(create_date__gte=yesterday).count(),
        'today_story_count': Story.objects.filter(create_date__gte=yesterday).count(),
        'today_message_count': Conversation_message.objects.filter(create_date__gte=yesterday).count(),

        'user_with_new_password': Person.objects.filter(has_new_password=True).count(),
        'user_with_phone': Person.objects.filter(phone_number_verified=True).count(),

        'used_service_within_last_hour': User.objects.filter(last_login__gt=last_hour).count(),
        'used_service_within_24_hr': User.objects.filter(last_login__gt=yesterday).count(),
        'used_service_within_last_week': User.objects.filter(last_login__gt=last_week).count(),
        'used_service_within_last_month': User.objects.filter(last_login__gt=last_month).count(),
    })
