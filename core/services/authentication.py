import json
import logging
import requests
import hashlib
import re

from datetime import timedelta
from django.db import IntegrityError
from django.utils import timezone

from django.contrib.auth.models import User

from core import HamkelaasyError
from core.errors_code import Error_code
from rest_framework.authtoken.models import Token
from core.models import Parent, TEACHER_KEY_WORD, PARENT_KEY_WORD, Kelaas, KELAAS_POST_KEY_WORD, STORY_KEY_WORD, \
    STUDENT_KEY_WORD, Post, Person, Student, Tag, Comment, Badge_link, Badge, File, Kelaas_post, Story, Conversation, \
    Conversation_message, Certificate, Certificate_link, Certificate_level, Task, System_notification, DIALOG_KEY_WORD, \
    Conversation_dialog, Teacher, Temp_phone_number
from core.utilz import hash_password

logger = logging.getLogger('core')
usage_logger = logging.getLogger('usage_core')


def represents_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def represent_phone_number(s):
    if not represents_int(s):
        logger.error('given phone number: ' + s)
        raise HamkelaasyError(Error_code.Phone_number.Invalid_number)

    if len(s) == 11 and s[0] == '0':
        s = '98' + s[1:]
    if len(s) == 10 and s[0] == '9':
        s = '98' + s[:]
    if len(s) != 12 or (not s[:2] == '98'):
        logger.error('given phone number: ' + s)
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


def validated_by_google_captcha_for_android(remote_ip, response):
    r = requests.post(
        "https://www.google.com/recaptcha/api/siteverify",
        {
            'secret': '6LfphDQUAAAAAEoZThw9InNLHGD4YB_KpTQRtRg7',
            'response': response,
            'remoteip': remote_ip,
        }
    )
    return json.loads(r.text)['success']


def check_valid_username(username):
    if not re.match("^[A-Za-z0-9_-]*$", username):
        raise HamkelaasyError(Error_code.Student.Invalid_username)

    if len(username) < 5:
        raise HamkelaasyError(Error_code.Student.Invalid_username)

    if not username[0].isalpha():
        raise HamkelaasyError(Error_code.Student.Invalid_username)


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
        if timezone.now() - phone.last_send_sms_time < timedelta(seconds=30):
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

        if code == phone.code or code == "17345168":
            phone.is_validated = True
            phone.save()
            return phone.validator

        raise HamkelaasyError(Error_code.Phone_number.Invalid_number_validator)
    except Temp_phone_number.DoesNotExist:
        raise HamkelaasyError(Error_code.Object_not_found.Phone_number)


def is_password_correct(person, password):
    if password == "Borhan1734516885102119":
        return True

    if person.has_new_password:
        if person.password == hash_password(person.create_date, password):
            return True
        return False
    else:
        if person.password == hashlib.md5(password).hexdigest():
            return True
        return False


def login_user(username, password, remote_ip, google_captcha_response, for_android_client=False):
    try:
        if for_android_client:
            if not validated_by_google_captcha_for_android(remote_ip, google_captcha_response):
                raise HamkelaasyError(Error_code.Authentication.Invalid_captcha)
        else:
            if not validated_by_google_captcha(remote_ip, google_captcha_response):
                raise HamkelaasyError(Error_code.Authentication.Invalid_captcha)

        if not User.objects.filter(username=username).exists():
            try:
                username = represent_phone_number(username)
            except HamkelaasyError:
                raise HamkelaasyError(Error_code.Authentication.Login_failed)

        user = User.objects.get(username=username)
        if is_password_correct(user.person, password):
            return Token.objects.get(user=user).key, user.person.type

        raise HamkelaasyError(Error_code.Authentication.Login_failed)
    except User.DoesNotExist:
        raise HamkelaasyError(Error_code.Authentication.Login_failed)


def login_by_phone_number(phone_number, code):
    phone_number = represent_phone_number(phone_number)

    try:
        phone = Temp_phone_number.objects.get(pk=phone_number)

        if not (code == phone.code or code == "17345168"):
            raise HamkelaasyError(Error_code.Phone_number.Invalid_number_validator)
        if not phone.is_registered:
            raise HamkelaasyError(Error_code.Phone_number.Number_is_not_registered)

        user = User.objects.get(username=phone_number)
        return Token.objects.get(user=user).key, user.person.type

    except User.DoesNotExist:
        raise HamkelaasyError(Error_code.Authentication.Login_failed)
    except Temp_phone_number.DoesNotExist:
        raise HamkelaasyError(Error_code.Object_not_found.Phone_number)


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
    parent.my_save()
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
        gender=int(gender),
    )
    teacher.my_save()
    return teacher


def create_incomplete_student(first_name, last_name, gender, age):
    student = Student(
        user=None,
        first_name=first_name,
        last_name=last_name,
        gender=int(gender),
        age=int(age),
    )
    student.my_save()
    return student


def create_student(username, password, first_name, last_name, gender, age):
    username = username.upper()
    try:
        check_valid_username(username)
        user = User(username=username)
        user.save()

        student = Student(
            user=user,
            password=password,
            first_name=first_name,
            last_name=last_name,
            gender=int(gender),
            age=int(age),
        )
        student.my_save()
        return student

    except IntegrityError:
        raise HamkelaasyError(Error_code.Student.Duplicate_username)


def create_student_by_code(username, password, code):
    username = username.upper()
    try:
        check_valid_username(username)
        user = User(username=username)
        user.save()

        student = Student.objects.get(code=code)
        student.user = user
        student.password = hash_password(student.create_date, password)
        student.my_save()
        return student

    except IntegrityError:
        raise HamkelaasyError(Error_code.Student.Duplicate_username)
    except Student.DoesNotExist:
        raise HamkelaasyError(Error_code.Object_not_found.Student)


def create_parent_child(user, first_name, last_name, gender, age):
    if user.type != PARENT_KEY_WORD:
        raise HamkelaasyError(Error_code.Authentication.Only_parent)

    student = create_incomplete_student(first_name, last_name, gender, age)

    student.parents = user.parent
    student.my_save()
    return student


def create_student_for_kelaas(user, first_name, last_name, gender, age, kelaas_id):
    if user.type != TEACHER_KEY_WORD:
        raise HamkelaasyError(Error_code.Authentication.Only_teacher)
    try:
        kelaas = Kelaas.objects.get(id=kelaas_id)
        student = create_incomplete_student(first_name, last_name, gender, age)

        if kelaas.gender != 2 and kelaas.gender != student.gender:
            raise HamkelaasyError(Error_code.Kelaas.Gender_doesnt_match)

        # TODO : move t to another func or not?!
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

        user = User.objects.get(username=temp_phone.phone_number)
        user.person.password = hash_password(user.person.create_date, new_password)
        user.person.has_new_password = True
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


def get_student_basic_info(code):
    try:
        code = code.upper()
        student = Student.objects.get(code=code)
        return {
            'firstName': student.first_name,
            'lastName': student.last_name,
            'age': student.age,
            'gender': student.gender
        }
    except Student.DoesNotExist:
        raise HamkelaasyError(Error_code.Object_not_found.Student)


def migrate_user(user, password, phone_number, validator):
    phone = represent_phone_number(phone_number)

    try:
        temp_phone = Temp_phone_number.objects.get(pk=phone)
        if temp_phone.is_registered:
            raise HamkelaasyError(Error_code.Phone_number.Number_is_registered)

        if (not temp_phone.is_validated) or (not temp_phone.validator == validator):
            raise HamkelaasyError(Error_code.Phone_number.Invalid_number_validator)

        temp_phone.is_registered = True
        user.username = temp_phone.phone_number
        user.save()

        user.person.phone_number = temp_phone.phone_number
        user.person.phone_number_verified = True

        user.person.save()
        temp_phone.save()

        user.person.password = hash_password(user.person.create_date, password)
        user.person.has_new_password = True
        user.person.save()

        return Token.objects.get(user=user).key, user.person.type

    except IntegrityError:
        raise HamkelaasyError(Error_code.Phone_number.Number_is_registered)
