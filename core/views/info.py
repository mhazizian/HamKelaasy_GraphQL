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

from django.http import HttpResponse

logger = logging.getLogger('core')


def info(request):
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
    })
