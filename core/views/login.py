# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import logging

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

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
        phone_number = int(phone_number)

        # send sms to given phone number
    except ValueError:
        pass

@csrf_exempt
def validate_phone_number(request):
    data = json.loads(request.body)
    try:
        phone_number = data.get('phone', '')
        code = data.get('code', '')

        # validate given code and phone number


    except:
        pass

def new_signup_user(request):
    pass
