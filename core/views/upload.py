# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json

from django.http import HttpResponse
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from core.models import File


@api_view(['POST'])
@parser_classes((MultiPartParser, FormParser))
def upload_file(request):
    if not request.user.is_authenticated:
        return HttpResponse('user not authenticated', status=401)

    if 'data' in request.FILES:
        input_file = request.FILES['data']
        f = File(
            title=request.POST.get('title', input_file.name),
            description=request.POST.get('description', 'بدون توضیح'),
            data=input_file
        )
        f.owner = request.user.person
        f.save()

        return HttpResponse(json.dumps({
            'data': {
                'id': f.id,
                'url': f.url,
                'title': f.title
            }
        }), content_type='application/json', status=202)

    return HttpResponse(json.dumps({
        'errors': [
            {
                'message': 'bad_file_input'
            }
        ]
    }), content_type='application/json', status=400)
