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
        return HttpResponse('user not authenticated', status=401)

    if request.method == "POST":
        data = json.loads(request.body)

        res = schema.execute(data.get('query', ''), context_value=request)
        if res.errors:
            return HttpResponse("bad data input", status=400)

        return HttpResponse(json.dumps(res.data), content_type='application/json', status=200)
    return HttpResponse("not post method!", status=405)