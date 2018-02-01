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
            "school_name": "سراج",
            "description": klass.description,
            "create_date": int(time.mktime(klass.create_date.timetuple())),
            "gender": gender,
            "teacher_id": klass.teacher_id,
            "students_id": [student.id for student in klass.students.all()],
        }
        res.append(obj)

    return HttpResponse(json.dumps(res, indent=4))
