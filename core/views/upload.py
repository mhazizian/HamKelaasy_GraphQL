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

    # if 'data' in request.FILES:
    files = []
    for uploaded_file in request.FILES.getlist('data'):
        f = File(
            # title=request.POST.get('title', uploaded_file.name),
            title=uploaded_file.name,
            description=request.POST.get('description', 'بدون توضیح'),
            data=uploaded_file
        )
        f.owner = request.user.person
        f.save()
        files.append(f.id)

    return HttpResponse(json.dumps({
        'id': ','.join([str(f) for f in files]),
        # 'url': f.url,
        # 'title': f.title
    }), status=202)
    # return HttpResponse('bad data input', status=400)