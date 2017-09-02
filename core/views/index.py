# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.contrib.auth.models import User
from django.http import HttpResponse
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from core.models import Person, Teacher, Student, Parent
from core.models import STUDENT_KEY_WORD, TEACHER_KEY_WORD, PARENT_KEY_WORD

from core.schema import schema


# Create your views here.

@api_view()
def index(request):
    # access token checking....
    if not request.user.is_authenticated:
        return HttpResponse('bad')
    # res = schema.execute(request.POST['query'])
    res = schema.execute(
        """
        {
            person{
             firstName
            }
        }
        """
    )
    if res.errors:
        return HttpResponse(json.dumps(res.errors))
    return HttpResponse(json.dumps(res.data))


# @api_view()
def test(request):
    print Token.objects.get(user=User.objects.get(username="mha")).key
    # s = Student(user=User.objects.get(username="admin"), first_name="ali", fard_access_token="1345678")
    # s.save()
    # p = Person(username="salam", first_name="ali", fard_access_token="12312341234")
    # p.save()
    # print (request.user)
    return HttpResponse("salam ")


def signup(request):
    res = {}
    try:
        data = json.loads(request.POST['data'])

        username = data['userName']
        first_name = data['firstName']
        last_name = data['lastName']
        email = data['email']
        gender = int(data['gender'])
        fard_access_token = data['accessToken']

        if User.objects.filter(username=username).exists():
            res['type'] = "error"
            res['message'] = "username is not available"
            return HttpResponse(json.dumps(res))
        user = User(username=username)
        user.save()

        type = data['type']

        if type == STUDENT_KEY_WORD:
            age = int(data['age'])
            nickname = data['nickName']

            student = Student(
                user=user,
                first_name=first_name,
                last_name=last_name,
                email=email, gender=gender,
                fard_access_token=fard_access_token,
                age=age,
                nickname=nickname
            )
            student.save()
        if type == TEACHER_KEY_WORD:
            teacher = Teacher(
                user=user,
                first_name=first_name,
                last_name=last_name,
                gender=gender,
                email=email,
                fard_access_token=fard_access_token,
            )
            teacher.save()
        if type == PARENT_KEY_WORD:
            parent = Parent(
                user=user,
                first_name=first_name,
                last_name=last_name,
                email=email,
                fard_access_token=fard_access_token,
            )
            parent.save()

        res['type'] = "success"
        res['token'] = Token.objects.get(user=user).key
        return HttpResponse(json.dumps(res))
    except:
        res['type'] = "error"
        res['message'] = "bad data input"
        return HttpResponse(json.dumps(res))
