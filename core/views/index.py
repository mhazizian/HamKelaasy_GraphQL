# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from collections import OrderedDict

from django.http import HttpResponse
from graphql import GraphQLError

from core.schema import schema


# Create your views here.


def index(request):
    # access token checking....

    # res = schema.execute(request.POST['query'])
    res = schema.execute(
        """
        {
            person{
             firstName
            }
        }
        """
    )
    if res.errors:
        return HttpResponse(json.dumps(res.errors))
    return HttpResponse(json.dumps(res.data))


def exist_check(request):
    if request.method == 'POST':
        pass
