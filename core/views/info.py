# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import requests
from django.shortcuts import render

import core.services as services
from django.db import connection

from core.utilz import hash_password
import json
import logging
import random

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from core.models import *
from datetime import datetime
from datetime import timedelta
from django.http import HttpResponse

logger = logging.getLogger('core')


def info(request):
    time = datetime.now() - timedelta(days=1)

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

        'today_user_count': Person.objects.filter(create_date__gte=time).count(),
        'today_parent_count': Parent.objects.filter(create_date__gte=time).count(),
        'today_student_count': Student.objects.filter(create_date__gte=time).count(),
        'today_teacher_count': Teacher.objects.filter(create_date__gte=time).count(),
        'today_kelaas_count': Kelaas.objects.filter(create_date__gte=time).count(),
        'today_story_count': Story.objects.filter(create_date__gte=time).count(),
        'today_message_count': Conversation_message.objects.filter(create_date__gte=time).count(),
    })
