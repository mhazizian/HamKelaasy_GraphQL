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


def migrate_class(request):
    res = []
    for klass in Kelaas.objects.all():

        if klass.gender == 1:
            gender = "M"
        if klass.gender == 0:
            gender = "F"
        if klass.gender == 2:
            gender = "B"

        obj = {
            "id": klass.id,
            "title": klass.title,
            "school_name": "S1",
            "description": klass.description,
            "create_date": int(time.mktime(klass.create_date.timetuple())),
            "gender": gender,

            "has_new_password": person.has_new_password,

            "first_name": person.first_name,
            "last_name": person.last_name,
            "email": person.email,
            "phone_number": person.phone_number if person.phone_number != "" else None,
            "last_login": last_login,
            'gender': gender,

            "is_student": person.type == STUDENT_KEY_WORD,
            "is_teacher": person.type == TEACHER_KEY_WORD,
            "is_parent": person.type == PARENT_KEY_WORD,

            "parent": parent
        }
        res.append(obj)

    return HttpResponse(json.dumps(res, indent=4))
