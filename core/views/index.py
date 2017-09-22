# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json

from core.graphql_utilz import get_status_code, get_pretty_response
from Hamkelaasy_graphQL.schema import schema

from django.contrib.auth.models import update_last_login
from rest_framework.decorators import api_view
from django.http import HttpResponse


@api_view(['POST'])
def index(request):
    if not request.user.is_authenticated or not hasattr(request.user, 'person'):
        return HttpResponse('user not authenticated', status=401)
    data = json.loads(request.body)
    update_last_login(None, request.user)

    print "_______________________________________________________"
    print ">>> request:"
    print data.get('query', '')
    print data.get('variables', None)
    print ">>> response:"

    res = schema.execute(
        data.get('query', ''),
        context_value=request,
        operation_name=data.get('operationName', None),
        variable_values=data.get('variables', None),
    )

    response = get_pretty_response(res)
    status_code = get_status_code(res)

    print json.dumps(response, indent=4, sort_keys=True)

    return HttpResponse(
        json.dumps(response),
        status=status_code,
        content_type='application/json',
    )


@api_view(['POST', 'GET'])
def logout(request):
    # TODO expire given token
    return HttpResponse('')
