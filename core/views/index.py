# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import logging

from core.utilz import get_status_code, get_pretty_response
from Hamkelaasy_graphQL.schema import schema

from django.contrib.auth.models import update_last_login
from rest_framework.decorators import api_view
from django.http import HttpResponse

logger = logging.getLogger('core')


@api_view(['POST'])
def index(request):
    if not request.user.is_authenticated or not hasattr(request.user, 'person'):
        return HttpResponse(4011)
    data = json.loads(request.body)

    res = schema.execute(
        data.get('query', ''),
        context_value=request,
        operation_name=data.get('operationName', None),
        variable_values=data.get('variables', None),
    )

    response = get_pretty_response(res)
    status_code = get_status_code(res)

    if status_code != 200:
        logger.info(
            '\nbegin >=============================================\n'
            + 'user:\n'
            + unicode(request.user.username)
            + ' | type: '
            + unicode(request.user.person.type)
            + '\n>>> request:\n'
            + unicode(data.get('query', ''))
            + '\n_____var_____\n'
            + unicode(data.get('variables', None))
            + '\n>>> response:\n'
            + unicode(json.dumps(response, indent=4, sort_keys=True))
            + '\nend >=============================================\n'
        )

    update_last_login(None, request.user)
    return HttpResponse(
        unicode(json.dumps(response)),
        status=status_code,
        content_type='application/json',
    )


@api_view(['POST', 'GET'])
def logout(request):
    # TODO expire given token
    return HttpResponse('')


from core.errors_code import errors


def error_doc(request):
    return HttpResponse(
        '<html><body><pre><code>'
        + json.dumps(errors, indent=4, sort_keys=True)
        + '</code></pre></body></html>'
    )
