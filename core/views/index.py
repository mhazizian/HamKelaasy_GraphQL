# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser

from Hamkelaasy_graphQL.schema import schema
from core.models import File


@api_view(['POST'])
def index(request):
    if not request.user.is_authenticated:
        return HttpResponse('user not authenticated', status=401)

    if request.method == "POST":
        data = json.loads(request.body)

        res = schema.execute(data.get('query', ''), context_value=request)
        if res.errors:
            print res.errors[0].message
            return HttpResponse(res.errors[0].message, status=400)
        return HttpResponse(json.dumps(res.data), content_type='application/json', status=200)

    return HttpResponse("not post method!", status=405)


@api_view(['POST', 'GET'])
@parser_classes((MultiPartParser, FormParser))
def upload_file(request):
    if not request.user.is_authenticated:
        return HttpResponse('user not authenticated', status=401)

    if 'data' in request.FILES:
        uploaded_file = request.FILES['data']

        f = File(
            title=request.POST.get('title', uploaded_file.name),
            description=request.POST.get('description', 'بدون توضیح'),
            data=uploaded_file
        )
        f.owner = request.user.person
        f.save()

        return HttpResponse(json.dumps({
            'id': f.id,
            'url': f.url,
            'title': f.title
        }), status=202)
    return HttpResponse('bad data input', status=400)
