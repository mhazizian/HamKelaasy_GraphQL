# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import logging

from django.http import HttpResponse
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from core.models import File

logger = logging.getLogger('core')


@api_view(['POST'])
@parser_classes((MultiPartParser, FormParser))
def upload_file(request):
    if not request.user.is_authenticated:
        return HttpResponse('user not authenticated', status=401)

    if 'data' in request.FILES:
        try:
            input_file = request.FILES['data']
            f = File.create(
                input_file=input_file,
                owner=request.user.person,
                title=request.POST.get('title', ""),
                description=request.POST.get('description', ''),
            )
            return HttpResponse(
                unicode(json.dumps({
                    'data': {
                        'id': f.id,
                        'url': f.url,
                        'title': f.title
                    }
                })),
                content_type='application/json',
                status=202
            )
        except Exception as e:
            logger.exception(
                '\nbegin >=============================================\n'
                + 'user:\n' + unicode(request.user.username)
                + '\nerror happend on UPLOAD file\n'
                + e.message
            )

    logger.warning(
        '\nbegin >=============================================\n'
        + 'user:\n'
        + unicode(request.user.username)
        + ' | type: '
        + unicode(request.user.person.type)
        + 'requested to upload file without providing appropriate file'
        + '\nend >=============================================\n'
    )
    return HttpResponse(

        unicode(json.dumps({
            'errors': [
                {
                    'message': 'bad_file_input'
                }
            ]
        })),
        content_type='application/json',
        status=400
    )
