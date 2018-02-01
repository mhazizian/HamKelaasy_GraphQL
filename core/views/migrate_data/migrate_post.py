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


def migrate_post(request):
    res = []
    for post in Story.objects.all():
        obj = {
            "title": post.title,
            "description": post.description,
            "create_date": int(time.mktime(post.create_date.timetuple())),
            "type": "S",
            "klass_is": post.kelaas_id,
            "writer_id": post.owner_id,
            "files": [pic.id for pic in post.pics.all()],
        }
        res.append(obj)

    for post in Kelaas_post.objects.all():
        obj = {
            "title": post.title,
            "description": post.description,
            "create_date": int(time.mktime(post.create_date.timetuple())),
            "type": "A",
            "klass_is": post.kelaas_id,
            "writer_id": post.owner_id,
            "files": [file.id for file in post.files.all()],
        }
        res.append(obj)

    return HttpResponse(json.dumps(res))
