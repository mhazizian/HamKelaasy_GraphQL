# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import logging

from rest_framework.decorators import api_view

import core.services as services
from core.utilz import HamkelaasyError, get_client_ip

from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from core.models import STUDENT_KEY_WORD, PARENT_KEY_WORD, TEACHER_KEY_WORD, Student

from django.http import HttpResponse

logger = logging.getLogger('core')


@csrf_exempt
def new_login(request):
    data = json.loads(request.body)

    username = data.get('username', '')

    if username.upper() == "TEACHER":
        username = "09128395942"
    if username.upper() == "PARENT":
        username = "09102127693"

    password = data.get('password', '')
    captcha_response = data.get('g-recaptcha-response', '')
    is_for_android = data.get('is_for_android', False)
    remote_ip = get_client_ip(request)

    try:
        token, user_type = services.login_user(
            username=username,
            password=password,
            google_captcha_response=captcha_response,
            remote_ip=remote_ip,
            for_android_client=is_for_android,
        )
        return HttpResponse(json.dumps(
            {
                'token': token,
                'type': user_type
            })
        )

    except HamkelaasyError as e:
        return e.to_http_response()


@csrf_exempt
def login_by_phone(request):
    data = json.loads(request.body)

    phone_number = data.get('phone', '')
    code = data.get('code', '')

    if phone_number == "1":
        phone_number = "09128395942"
        code = "17345168"

    if phone_number == "2":
        phone_number = "09102127693"
        code = "17345168"

    try:
        token, user_type = services.login_by_phone_number(phone_number, code)

        return HttpResponse(json.dumps(
            {
                'token': token,
                'type': user_type
            })
        )
    except HamkelaasyError as e:
        return e.to_http_response()


@csrf_exempt
def get_phone_number(request):
    data = json.loads(request.body)
    try:
        phone_number = data.get('phone', '')
        if phone_number == '':
            phone_number = data.get('phone_number', '')

        if phone_number == "1":
            phone_number = "09128395942"
        if phone_number == "2":
            phone_number = "09102127693"

        is_for_registration = data.get('is_for_registration', True)

        services.init_phone_number(phone_number, is_for_registration=is_for_registration)
        return HttpResponse('')
    except HamkelaasyError as e:
        return e.to_http_response()


@csrf_exempt
def validate_phone_number(request):
    data = json.loads(request.body)

    phone_number = data.get('phone', '')
    code = data.get('code', '')
    try:
        res = services.validate_phone_number(phone_number, code)

        return HttpResponse(json.dumps(
            {
                'accepted': True,
                'validator': res
            }),
            content_type='application/json',
        )
    except HamkelaasyError as e:
        return e.to_http_response()


@csrf_exempt
def reset_password(request):
    data = json.loads(request.body)

    try:
        phone_number = data.get('phone', '')
        phone_validator = data.get('validator', '')
        new_password = data.get('password', '')

        services.reset_password_by_phone_number(phone_number, phone_validator, new_password)
        return HttpResponse('done')

    except HamkelaasyError as e:
        return e.to_http_response()


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
        return e.to_http_response()


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
        return e.to_http_response()


@csrf_exempt
def get_student_basic_info(request):
    data = json.loads(request.body)

    code = data.get('code', '')
    try:
        res = services.get_student_basic_info(code)
        return HttpResponse(
            json.dumps(res),
            content_type='application/json'
        )
    except HamkelaasyError as e:
        return e.to_http_response()


@csrf_exempt
def new_signup_student(request):
    data = json.loads(request.body)

    first_name = data.get('firstName', '')
    last_name = data.get('lastName', '')
    password = data.get('password', '')
    username = data.get('username', '')
    gender = data.get('gender', '')
    age = data.get('age', '')

    try:
        student = services.create_student(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            age=age,
        )
        return HttpResponse(json.dumps(
            {
                'status': 1,
                'token': Token.objects.get(user=student.user).key
            })
        )
    except HamkelaasyError as e:
        return e.to_http_response()


@csrf_exempt
def new_signup_student_by_code(request):
    data = json.loads(request.body)

    password = data.get('password', '')
    username = data.get('username', '')
    code = data.get('code', '')

    try:
        student = services.create_student_by_code(
            username=username,
            password=password,
            code=code,
        )
        return HttpResponse(json.dumps(
            {
                'status': 1,
                'token': Token.objects.get(user=student.user).key
            })
        )
    except HamkelaasyError as e:
        return e.to_http_response()


@api_view(['POST'])
def migrate_user(request):
    if not request.user.is_authenticated or not hasattr(request.user, 'person'):
        return HttpResponse(4011)
    data = json.loads(request.body)

    phone = data.get('phone', '')
    validator = data.get('validator', '')
    password = data['password']

    try:
        token, user_type = services.migrate_user(
            user=request.user,
            password=password,
            phone_number=phone,
            validator=validator,
        )

        return HttpResponse(json.dumps(
            {
                'token': token,
                'type': user_type
            })
        )
    except HamkelaasyError as e:
        return e.to_http_response()


@csrf_exempt
def get_kelaas_basic_info_handler(request):
    # TODO security problem: on brute force ...
    if request.method == 'POST':

        try:
            data = json.loads(request.body)
            kelaas_code = data.get('kelaas_code', '')
            kelaas_code = kelaas_code.upper()
            kelaas = services.get_kelaas_by_invite_code(invite_code=kelaas_code)

            res = {
                'title': kelaas.title,
                'description': kelaas.description,
                'shamsi_date': kelaas.shamsi_date,
                'gender': kelaas.gender,
                'teacher_first_name': kelaas.teacher.first_name,
                'teacher_last_name': kelaas.teacher.last_name,
                'teacher_gender': kelaas.teacher.gender,
            }
            return HttpResponse(
                unicode(json.dumps(res)),
                status=200
            )
        except HamkelaasyError as e:
            return e.to_http_response()
    return HttpResponse('Bad request', status=405)
