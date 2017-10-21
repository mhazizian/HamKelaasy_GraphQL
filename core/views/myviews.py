# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import requests

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

logger = logging.getLogger('core')


def my_view(request):
    if (not request.user.is_authenticated) or request.user.username != 'admin':
        return HttpResponse('')

    # for teacher in Teacher.objects.all():
    #     teacher.gender = 1
    #     teacher.save()
    #
    # return HttpResponse('hi')

    # user = User.objects.get(username='kazem')
    # token = Token.objects.get(user=user).key
    # return HttpResponse(str(token))

    student = Student.objects.get(id=165)
    services.join_kelaas(user=student, invite_code='K3MOO')



    # for person in Person.objects.all():
    #     if person.has_new_password:
    #         continue
    #     if not person.user:
    #         continue
    #
    #     r = requests.post(
    #         "http://fard.ir/api.php",
    #         {
    #             'token': 'salampedi',
    #             'username': person.user.username,
    #         }
    #     )
    #
    #     person.password = r.text
    #     logger.info('done for : ' + person.user.username)
    #     person.save()

    # for kelaas in Kelaas.objects.all():
    #     kelaas.kelaas_pic.name = 'kelaas/default.png'
    #     kelaas.save()
    #
    # return HttpResponse('salamm')

    # logger.info('done')

    # user = User.objects.get(username='989102127693')
    # c = 0
    # for conv in Conversation.objects.all():
    #     if conv.member_count < 2:
    #         c = c + 1

    # parent = Parent.objects.get(id=6)
    # parent.first_name = 'why?!'
    # parent.save()

    # user = User(username='9102127693')
    # user.save()
    #
    # parent = Parent(
    #     user=user,
    #     first_name='ali',
    #     last_name='jamali',
    #     password='mohammad',
    #     phone_number='9102127693',
    #     phone_number_verified=True,
    # )
    # parent.my_save()
    #
    # user1 = User(username='112211')
    # user1.save()
    #
    # student = Student(
    #     user=user1,
    #     password='mohammad',
    #     first_name='mh',
    #     last_name='az',
    #     gender=int(1),
    #     age=int(15),
    # )
    # student.my_save()
    #
    # logger.info('created')
    #
    # student.parents = parent
    # student.my_save()

    # for student in Student.objects.all():
    #     if student.gender != 1:
    #         student.gender = 1
    #         student.save()


    # cursor = connection.cursor()
    # cursor.execute("SELECT setval('perosn_id_seq', (SELECT MAX(id) FROM Persons)+1)")

    # student = Student.objects.filter(id=187).update(gendes=1)
    # student.gender = 1
    # student.update()

    # return HttpResponse('salammm:Ddm!')
    # return HttpResponse(
    #     str(student.gender) + " " + student.first_name + " " + student.last_name + " " + student.user.username + " " + str(
    #         student.create_date))
