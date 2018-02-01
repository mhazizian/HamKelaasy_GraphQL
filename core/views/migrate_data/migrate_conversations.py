# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import hashlib

import requests
import time

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


def migrate_conversations(request):
    res = []
    for message in Conversation_message.objects.all().order_by('create_date'):
        conversation = message.conversation
        if conversation.type == GROUP_KEY_WORD:
            continue

        parent_id = None
        teacher_id = None
        if conversation.members.all()[0].type == TEACHER_KEY_WORD:
            teacher_id = conversation.members.all()[0].id
        if conversation.members.all()[0].type == PARENT_KEY_WORD:
            parent_id = conversation.members.all()[0].id
        if conversation.members.all()[1].type == TEACHER_KEY_WORD:
            teacher_id = conversation.members.all()[1].id
        if conversation.members.all()[1].type == PARENT_KEY_WORD:
            parent_id = conversation.members.all()[1].id

        obj = {
            # "id": conversation.id,
            "teacher_id": teacher_id,
            "parent_id": parent_id,

            "sender_id": message.writer_id,
            "text": message.body,
            "create_date": int(time.mktime(message.create_date.timetuple()))
        }
        res.append(obj)

    return HttpResponse(json.dumps(res, indent=4))
