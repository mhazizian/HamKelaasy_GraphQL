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


def migrate_user(request):
    res = []
    for person in Person.objects.all():
        if person.user:
            if person.user.username == "admin":
                continue
            # if person.user.username == "989102127693":
            #     continue
            # if person.user.username == "989128395942":
            #     continue

            if person.user.username == "phone989015281382":
                person.phone_number = None

            username = person.user.username
            if person.user.last_login:
                last_login = int(time.mktime(person.user.last_login.timetuple()))
            else:
                last_login = None
        else:
            username = None
            last_login = None

        parent = None
        if person.type == STUDENT_KEY_WORD:
            parent = person.student.parents_id
            # if parent == 4 or parent == 6:
            #     continue

        gender = '0'
        if person.type == TEACHER_KEY_WORD:
            gender = person.teacher.gender
        if person.type == STUDENT_KEY_WORD:
            gender = person.student.gender

        if gender == 1 or gender == "1":
            gender = "M"
        if gender == 0 or gender == "0":
            gender = "F"
        if not gender:
            gender = "M"

        obj = {
            "id": person.id,
            "username": username,

            "password": person.password,
            "has_new_password": person.has_new_password,

            "first_name": person.first_name,
            "last_name": person.last_name,
            "email": person.email,
            "phone_number": person.phone_number if person.phone_number != "" else None,
            "last_login": last_login,
            "create_date": int(time.mktime(person.create_date.timetuple())),
            'gender': gender,

            "is_student": person.type == STUDENT_KEY_WORD,
            "is_teacher": person.type == TEACHER_KEY_WORD,
            "is_parent": person.type == PARENT_KEY_WORD,

            "parent": parent
        }
        res.append(obj)

    return HttpResponse(json.dumps(res, indent=4))
