# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.http import HttpResponse
from core import myGraphQLError
from rest_framework.decorators import api_view
from Hamkelaasy_graphQL.schema import schema


@api_view(['POST'])
def index(request):
    print "_______________________________________________________"
    if not request.user.is_authenticated or not hasattr(request.user, 'person'):
        return HttpResponse('user not authenticated', status=401)

    if request.method == "POST":
        data = json.loads(request.body)
        print ">>> request:"
        print data.get('query', '')

        res = schema.execute(
            data.get('query', ''),
            context_value=request,
            variable_values=data.get('variables', None),
            operation_name=data.get('operationName', None),
        )
        responde = {}
        if res.errors:
            print res.errors

            responde['errors'] = res.errors
            responde['data'] = ''

            if isinstance(res.errors[0], myGraphQLError):
                # TODO change 'res.errors[0].message' to 'json.dumps(responde)'
                return HttpResponse(
                    res.errors[0].message,
                    status=res.errors[0].original_error.status,
                    content_type='application/json',
                )
            else:
                # TODO change 'res.errors[0].message' to 'json.dumps(responde)'
                return HttpResponse(
                    res.errors[0].message,
                    status=400,
                    content_type='application/json',
                )

        responde['data'] = res.data

        print ">>> respond:"
        print json.dumps(res.data, indent=4, sort_keys=True)
        # print json.dumps(responde, indent=4, sort_keys=True)

        # TODO change the format of responde
        return HttpResponse(json.dumps(res.data), content_type='application/json', status=200)

    return HttpResponse("not post method!", status=405)


@api_view(['POST'])
def logout(request):
    # TODO expire given token
    return HttpResponse('')
