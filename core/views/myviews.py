# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import logging
import random

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from core.models import *

from django.http import HttpResponse

logger = logging.getLogger('core')


def my_view(request):
    for student in Student.objects.all():
        student.profile_pic.name = 'student/people' + str(random.randint(1, 11)) + '.png'
        student.save()

    return HttpResponse('done')
