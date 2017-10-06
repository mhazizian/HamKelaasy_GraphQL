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
    if (not request.user.is_authenticated) or request.user.username != 'admin':
        return HttpResponse('')

    conv = Conversation.objects.get(id=35)
    conv.delete()
    # c = 0
    # for conv in Conversation.objects.all():
    #     if conv.member_count < 2:
    #         c = c + 1

    return HttpResponse('')
