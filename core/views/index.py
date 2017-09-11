# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.http import HttpResponse
from rest_framework.decorators import api_view
from Hamkelaasy_graphQL.schema import schema


@api_view(['POST'])
def index(request):
    if not request.user.is_authenticated:
        return HttpResponse('user not authenticated', status=401)

    if request.method == "POST":
        data = json.loads(request.body)

        res = schema.execute(data.get('query', ''), context_value=request)
        if res.errors:
            return HttpResponse(res.errors[0].message, status=400)
        return HttpResponse(json.dumps(res.data), content_type='application/json', status=200)

    return HttpResponse("not post method!", status=405)


@api_view(['POST'])
def logout(request):
    # TODO expire given token
    return HttpResponse('')
