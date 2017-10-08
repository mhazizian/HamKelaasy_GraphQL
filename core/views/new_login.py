# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import logging

import core.services as services
from core.utilz import HamkelaasyError

from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from core.models import STUDENT_KEY_WORD, PARENT_KEY_WORD, TEACHER_KEY_WORD, Student

from django.http import HttpResponse

logger = logging.getLogger('core')


@csrf_exempt
def new_login(request):
    data = json.loads(request.body)

    username = data.get('username', '')
    password = data.get('password', '')

    try:
        token, user_type = services.login_user(username=username, password=password)
        return HttpResponse(json.dumps(
            {
                'token': token,
                'type': user_type
            }
        ))

    except HamkelaasyError as e:
        return e.get_http_response()


@csrf_exempt
def get_phone_number(request):
    data = json.loads(request.body)
    try:
        phone_number = data.get('phone', '')
        is_for_registration = data.get('is_for_registration', True)

        services.init_phone_number(phone_number, is_for_registration=is_for_registration)
        return HttpResponse('')
    except HamkelaasyError as e:
        return e.get_http_response()


@csrf_exempt
def validate_phone_number(request):
    data = json.loads(request.body)

    phone_number = data.get('phone', '')
    code = data.get('code', '')
    try:
        res = services.validate_phone_number(phone_number, code)

        return HttpResponse(json.dumps(
            {
                'response': True,
                'validator': res
            }),
            content_type='application/json',
        )
    except HamkelaasyError as e:
        return e.get_http_response()


@csrf_exempt
def reset_password(request):
    data = json.loads(request.body)

    try:
        phone_number = data.get('phone', '')
        phone_validator = data.get('validator', '')
        new_password = data.get('password', '')

        services.reset_password_by_phone_number(phone_number, phone_validator, new_password)
        return HttpResponse('')

    except HamkelaasyError as e:
        return e.get_http_response()


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
            password=password,
            type=PARENT_KEY_WORD
        )
        return HttpResponse(json.dumps(
            {
                'status': 1,
                'token': Token.objects.get(user=parent.user).key
            })
        )
    except HamkelaasyError as e:
        return e.get_http_response()


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
            password=password,
            type=TEACHER_KEY_WORD,
            gender=gender
        )
        return HttpResponse(json.dumps(
            {
                'status': 1,
                'token': Token.objects.get(user=parent.user).key
            })
        )
    except HamkelaasyError as e:
        return e.get_http_response()


@csrf_exempt
def get_student_basic_info(request):
    # TODO fix signature of this func
    data = json.loads(request.body)

    code = data.get('code', '')
    try:
        student = Student.objects.get(code=code)
        return HttpResponse(json.dumps(
            {
                'firstName': student.first_name,
                'lastName': student.last_name,
                'age': student.age,
                'gender': student.gender
            }),
            content_type='application/json'
        )
    except Student.DoesNotExist:
        pass
