# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import logging

import core.services as services

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from core.models import STUDENT_KEY_WORD, PARENT_KEY_WORD, TEACHER_KEY_WORD

from django.http import HttpResponse

logger = logging.getLogger('core')


@csrf_exempt
def new_login(request):
    data = json.loads(request.body)

    username = data.get('username', '')
    password = data.get('password', '')

    try:
        user = User.objects.get(username=username)
        if user.person.password == password:
            return HttpResponse(json.dumps({
                'token': Token.objects.get(user=user).key,
                'type': user.person.type
            }))
    except User.DoesNotExist:
        return HttpResponse('Invalid username or password', status=401)
    return HttpResponse('Invalid username or password', status=401)


@csrf_exempt
def get_phone_number(request):
    data = json.loads(request.body)
    try:
        phone_number = data.get('phone', '')
        services.init_phone_number(phone_number)
        return HttpResponse('')
    except Exception as e:
        return HttpResponse(e.message, status=400)


@csrf_exempt
def validate_phone_number(request):
    data = json.loads(request.body)

    phone_number = data.get('phone', '')
    code = data.get('code', '')

    res = services.validate_phone_number(phone_number, code)

    if res:
        return HttpResponse(json.dumps({
            'response': True,
            'validator': res
        }),
            content_type='application/json'
        )

    return HttpResponse(json.dumps({
        'response': False
    }),
        content_type='application/json'
    )


@csrf_exempt
def new_signup_parent(request):
    data = json.loads(request.body)

    phone_number = data.get('phone', '')
    phone_validator = data.get('validator', '')
    first_name = data.get('firstName', '')
    last_name = data.get('lastName', '')
    password = data.get('password', '')
    try:
        parent = services.create_user_PT(
            phone=phone_number,
            validator=phone_validator,
            first_name=first_name,
            last_name=last_name,
            pass_md5=password,
            type=PARENT_KEY_WORD
        )
        return HttpResponse(json.dumps(
            {
                'status': 1,
                'token': Token.objects.get(user=parent.user).key
            })
        )
    except Exception as e:
        return HttpResponse(json.dumps(
            {
                'status': 0
            }),
            status=400
        )



@csrf_exempt
def new_signup_teacher(request):
    data = json.loads(request.body)

    phone_number = data.get('phone', '')
    phone_validator = data.get('validator', '')
    first_name = data.get('firstName', '')
    last_name = data.get('lastName', '')
    password = data.get('password', '')
    gender = data.get('gender', '')
    try:
        parent = services.create_user_PT(
            phone=phone_number,
            validator=phone_validator,
            first_name=first_name,
            last_name=last_name,
            pass_md5=password,
            type=TEACHER_KEY_WORD,
            gender=gender
        )
        return HttpResponse(json.dumps(
            {
                'status': 1,
                'token': Token.objects.get(user=parent.user).key
            })
        )
    except Exception as e:
        return HttpResponse(json.dumps(
            {
                'status': 0
            }),
            status=400
        )
