import json
import logging
import binascii
import requests
import hashlib
import time

from datetime import timedelta
from django.db import IntegrityError
from django.utils import timezone

from django.contrib.auth.models import User

from Hamkelaasy_graphQL import settings
from core import HamkelaasyError
from core.errors_code import Error_code
from rest_framework.authtoken.models import Token
from core.models import Parent, TEACHER_KEY_WORD, PARENT_KEY_WORD, Kelaas, KELAAS_POST_KEY_WORD, STORY_KEY_WORD, \
    STUDENT_KEY_WORD, Post, Person, Student, Tag, Comment, Badge_link, Badge, File, Kelaas_post, Story, Conversation, \
    Conversation_message, Certificate, Certificate_link, Certificate_level, Task, System_notification, DIALOG_KEY_WORD, \
    Conversation_dialog, Teacher, Temp_phone_number
from core.utilz import hash_password

logger = logging.getLogger('core')


def represents_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def represent_phone_number(s):
    if not represents_int(s):
        raise HamkelaasyError(Error_code.Phone_number.Invalid_number)

    if len(s) == 11 and s[0] == '0':
        s = '98' + s[1:]
    if len(s) == 10 and s[0] == '9':
        s = '98' + s[:]
    if len(s) != 12 or (not s[:2] == '98'):
        raise HamkelaasyError(Error_code.Phone_number.Invalid_number)
    return s


def send_sms(phone_number, code):
    r = requests.post(
        "http://sms.3300.ir/services/wsSend.ashx",
        {
            'username': 'nbwa12826',
            'password': '260916',
            'mobile': phone_number,
            'message': unicode(code),
            'type': 2
        }
    )
    res = json.loads(r.text)
    if res['status'] < 0:
        return True
    if res['status'] == 103 or res['status'] == 1 or res['status'] == 2:
        raise HamkelaasyError(Error_code.Phone_number.Invalid_number)
    if res['status'] == 15:
        raise HamkelaasyError(Error_code.Phone_number.Server_in_development)

    raise HamkelaasyError(Error_code.Phone_number.Server_is_busy)


def validated_by_google_captcha(remote_ip, response):
    r = requests.post(
        "https://www.google.com/recaptcha/api/siteverify",
        {
            'secret': '6LeUCTQUAAAAAKhwMqGNCW36QT6mWF36QusyFDyt',
            'response': response,
            'remoteip': remote_ip,
        }
    )
    return json.loads(r.text)['success']

# __________________________________________________________________________________________
# __________________________________________________________________________________________


def init_phone_number(phone_number, is_for_registration=True):
    phone_number = represent_phone_number(phone_number)

    if Temp_phone_number.objects.filter(pk=phone_number).exists():
        phone = Temp_phone_number.objects.get(pk=phone_number)

        if is_for_registration and phone.is_registered:
            raise HamkelaasyError(Error_code.Phone_number.Number_is_registered)

        if (not is_for_registration) and (not phone.is_registered):
            raise HamkelaasyError(Error_code.Phone_number.Number_is_not_registered)

        # TODO change 10 sec to 60 sec in production.
        if timezone.now() - phone.last_send_sms_time < timedelta(seconds=10):
            raise HamkelaasyError(Error_code.Phone_number.Delay_required)

        phone.re_init()
    else:
        if not is_for_registration:
            raise HamkelaasyError(Error_code.Phone_number.Number_is_not_registered)

        phone = Temp_phone_number(phone_number=phone_number)
        phone.save()

    send_sms(phone_number=phone.phone_number, code=phone.code)


def validate_phone_number(phone_number, code):
    phone_number = represent_phone_number(phone_number)

    try:
        phone = Temp_phone_number.objects.get(pk=phone_number)

        if code == phone.code:
            phone.is_validated = True
            phone.save()
            return phone.validator

        raise HamkelaasyError(Error_code.Phone_number.Invalid_number_validator)
    except Temp_phone_number.DoesNotExist:
        raise HamkelaasyError(Error_code.Object_not_found.Phone_number)


def is_password_correct(person, password):
    if person.has_new_password:
        if person.password == hash_password(person.create_date, password):
            return True
        return False
    else:
        if person.password == hashlib.md5(password).digest():
            return True
        return False


def login_user(username, password, remote_ip, google_captcha_response):
    try:
        if not validated_by_google_captcha(remote_ip, google_captcha_response):
            raise HamkelaasyError(Error_code.Authentication.Invalid_captcha)

        if not User.objects.filter(username=username).exists():
            username = represent_phone_number(username)

        user = User.objects.get(username=username)
        if is_password_correct(user.person, password):
            return Token.objects.get(user=user).key, user.person.type

    except User.DoesNotExist:
        raise HamkelaasyError(Error_code.Authentication.Login_failed)


# _____________________________________________________________________________________
# _____________________________________________________________________________________


def create_parent(phone, first_name, last_name, password):
    user = User(username=phone)
    user.save()

    parent = Parent(
        user=user,
        first_name=first_name,
        last_name=last_name,
        password=password,
        phone_number=phone,
        phone_number_verified=True,
    )
    parent.save()
    return parent


def create_teacher(phone, first_name, last_name, password, gender):
    user = User(username=phone)
    user.save()

    teacher = Teacher(
        user=user,
        first_name=first_name,
        last_name=last_name,
        password=password,
        phone_number=phone,
        phone_number_verified=True,
        gender=gender,
    )
    teacher.save()
    return teacher


def create_incomplete_student(first_name, last_name, gender, age):
    student = Student(
        user=None,
        first_name=first_name,
        last_name=last_name,
        gender=gender,
        age=age,
    )
    student.save()
    return student


def create_parent_child(user, first_name, last_name, gender, age):
    if user.type != PARENT_KEY_WORD:
        raise HamkelaasyError(Error_code.Authentication.Only_parent)

    student = create_incomplete_student(first_name, last_name, gender, age)

    student.parents = user.parent
    student.save()
    return student


def create_student_for_kelaas(user, first_name, last_name, gender, age, kelaas_id):
    if user.type != TEACHER_KEY_WORD:
        raise HamkelaasyError(Error_code.Authentication.Only_teacher)
    try:
        kelaas = Kelaas.objects.get(id=kelaas_id)
        student = create_incomplete_student(first_name, last_name, gender, age)

        if kelaas.gender != 2 and kelaas.gender != student.gender:
            raise HamkelaasyError(Error_code.Kelaas.Gender_doesnt_match)

        kelaas.students.add(student)
        kelaas.save()
        return student
    except Kelaas.DoesNotExist:
        raise HamkelaasyError(Error_code.Object_not_found.Kelaas)


def reset_password_by_phone_number(phone_number, validator, new_password):
    phone = represent_phone_number(phone_number)

    try:
        temp_phone = Temp_phone_number.objects.get(pk=phone)
        if not temp_phone.is_registered:
            raise HamkelaasyError(Error_code.Phone_number.Number_is_not_registered)

        if (not temp_phone.is_validated) or (not temp_phone.validator == validator):
            raise HamkelaasyError(Error_code.Phone_number.Invalid_number_validator)

        user = User.objects.get(username=temp_phone.phone)
        user.person.password = new_password
        # TODO apply hashing
        user.person.save()

    except Temp_phone_number.DoesNotExist:
        raise HamkelaasyError(Error_code.Object_not_found.Phone_number)
    except User.DoesNotExist:
        raise HamkelaasyError(Error_code.Object_not_found.Person)


def create_user_PT(phone, validator, first_name, last_name, password, type, gender=1):
    phone = represent_phone_number(phone)

    try:
        temp_phone = Temp_phone_number.objects.get(pk=phone)
        if temp_phone.is_registered:
            raise HamkelaasyError(Error_code.Phone_number.Number_is_registered)

        if (not temp_phone.is_validated) or (not temp_phone.validator == validator):
            raise HamkelaasyError(Error_code.Phone_number.Invalid_number_validator)

        temp_phone.is_registered = True
        temp_phone.save()

        if type == TEACHER_KEY_WORD:
            return create_teacher(
                phone=phone,
                first_name=first_name,
                last_name=last_name,
                password=password,
                gender=gender
            )

        if type == PARENT_KEY_WORD:
            return create_parent(
                phone=phone,
                first_name=first_name,
                last_name=last_name,
                password=password,
            )

    except Temp_phone_number.DoesNotExist:
        raise HamkelaasyError(Error_code.Object_not_found.Phone_number)
    except IntegrityError:
        raise HamkelaasyError(Error_code.Phone_number.Number_is_registered)
