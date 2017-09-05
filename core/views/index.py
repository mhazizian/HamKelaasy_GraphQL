# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from core.models import Person, Teacher, Student, Parent, User_temp
from core.models import STUDENT_KEY_WORD, TEACHER_KEY_WORD, PARENT_KEY_WORD

from Hamkelaasy_graphQL.schema import schema
from core.views.fard_api import Fard_API


@api_view(['POST'])
@csrf_exempt
def index(request):
    if not request.user.is_authenticated:
        return HttpResponse('user not authenticated')

    if request.method == "POST":
        res = schema.execute(request.POST['query'], context_value=request)
        if res.errors:
            return HttpResponse(json.dumps(res.errors), content_type='application/json')
        return HttpResponse(json.dumps(res.data), content_type='application/json')
    return HttpResponse("not post method!")
