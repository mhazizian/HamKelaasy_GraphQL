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

        try:
            res = schema.execute(data.get('query', ''), context_value=request)
            print ">>> query done"

            print ">>> respond:"
            print json.dumps(res.data, indent=4, sort_keys=True)
            return HttpResponse(json.dumps(res.data), content_type='application/json', status=200)
        except myGraphQLError:
            if res.errors:
                print res.errors[0].message
                return HttpResponse(res.errors[0].message, status=400)

    return HttpResponse("not post method!", status=405)


@api_view(['POST'])
def logout(request):
    # TODO expire given token
    return HttpResponse('')
