# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from Hamkelaasy_graphQL.schema import schema
from core.models import File


@api_view(['POST'])
@csrf_exempt
def index(request):
    if not request.user.is_authenticated:
        return HttpResponse('user not authenticated')

    if request.method == "POST":
        res = schema.execute(request.POST.get('query', ""), context_value=request)
        if res.errors:
            return HttpResponse(json.dumps(res.errors), content_type='application/json')

        return HttpResponse(json.dumps(res.data), content_type='application/json')
    return HttpResponse("not post method!")


@api_view(['POST', 'GET', 'FILES'])
def upload_file(request):
    if not request.user.is_authenticated:
        return HttpResponse('user not authenticated')

    # improvment for later:
    #         1.upload i file for each request
    #         2.get file detile like title and description

    file = []
    for f in request.FILES.getlist('post-files'):
        temp = File(title=f.name, data=f)
        temp.owner = request.user.person
        temp.save()
        file.append(temp)
    return HttpResponse(json.dumps([f.id for f in file]))
