# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import logging

from rest_framework.decorators import api_view

import core.services as services

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from core.models import STORY_KEY_WORD, PARENT_KEY_WORD, TEACHER_KEY_WORD

from core.graphql_utilz import get_status_code, get_pretty_response
from Hamkelaasy_graphQL.schema import schema

from django.contrib.auth.models import update_last_login

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


@api_view(['POST'])
def new_signup_student_without_acc(request):
    if not request.user.is_authenticated or not hasattr(request.user, 'person'):
        return HttpResponse('user not authenticated', status=401)
    if not request.user.person.type == PARENT_KEY_WORD:
        return HttpResponse('you should be parent', status=403)

    data = json.loads(request.body)
