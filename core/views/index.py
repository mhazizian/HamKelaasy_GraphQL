# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import six

from core import myGraphQLError
from graphql import GraphQLError
from graphql.error import format_error as format_graphql_error

from Hamkelaasy_graphQL.schema import schema
from rest_framework.decorators import api_view
from django.http import HttpResponse


@api_view(['POST'])
def index(request):
    print "_______________________________________________________"
    if not request.user.is_authenticated or not hasattr(request.user, 'person'):
        return HttpResponse('user not authenticated', status=401)

    if request.method == "POST":
        data = json.loads(request.body)
        print ">>> request:"
        print data.get('query', '')
        print data.get('variables', None)
        print ">>> respond:"

        res = schema.execute(
            data.get('query', ''),
            context_value=request,
            operation_name=data.get('operationName', None),
            variable_values=data.get('variables', None),
        )
        response = {}
        if res.errors:

            response['errors'] = [format_error(e) for e in res.errors]
            response['data'] = res.data

            print json.dumps(response, indent=4, sort_keys=True)

            status_code = 400
            if isinstance(res.errors[0], myGraphQLError):
                status_code = res.errors[0].original_error.status

            # TODO change 'res.errors[0].message' to 'json.dumps(response)'
            return HttpResponse(
                res.errors[0].message,
                status=status_code,
                content_type='application/json',
            )

        response['data'] = res.data
        print json.dumps(response, indent=4, sort_keys=True)

        # TODO change the format of response
        return HttpResponse(json.dumps(res.data), content_type='application/json', status=200)

    return HttpResponse("not post method!", status=405)


@api_view(['POST', 'GET'])
def logout(request):
    # TODO expire given token

    return HttpResponse('')


def format_error(error):
    if isinstance(error, GraphQLError):
        return format_graphql_error(error)

    return {'message': six.text_type(error)}
