import hashlib
import json
import logging

import binascii
import six
import time

from Hamkelaasy_graphQL import settings
from graphql import GraphQLError

from core.errors_code import errors
from graphql.error import format_error as format_graphql_error
from django.http import HttpResponse

logger = logging.getLogger('core')


class HamkelaasyError(Exception):
    def __init__(self, error_code):
        self.error_code = error_code.value
        logger.error('hi bro :D')
        self.message = errors[error_code.value].get('message', '')
        self.status = errors[error_code.value].get('status', 400)
        logger.error('hi agin bro :D')

    def set_message(self, message):
        self.message = message

    def set_status_code(self, status_code):
        self.status = status_code

    def to_dictionary(self):
        return {
            'message': self.message,
            'code': self.error_code
        }

    def to_http_response(self):
        res = {'errors': [self.to_dictionary()]}
        return HttpResponse(
            unicode(json.dumps(res)),
            status=self.status,
            content_type='application/json',
        )


def hash_password(created_date, password):
    salt = settings.PUB_SALT + str(time.mktime(created_date.timetuple()))[:-2]
    res = hashlib.pbkdf2_hmac('sha256', password, salt, 100000)
    return binascii.hexlify(res)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_status_code(response):
    if response.errors:
        status_code = 400
        if hasattr(response.errors[0], 'original_error'):
            if isinstance(response.errors[0].original_error, HamkelaasyError):
                status_code = response.errors[0].original_error.status
        return status_code
    else:
        return 200


def get_pretty_response(response):
    res = {}
    if response.errors:
        res['errors'] = [format_error(e) for e in response.errors]

    res['data'] = response.data
    return res


def format_error(error):
    if hasattr(error, 'original_error'):
        if isinstance(error.original_error, HamkelaasyError):
            return error.original_error.to_dictionary()

    if isinstance(error, GraphQLError):
        return format_graphql_error(error)

    return {'message': six.text_type(error)}
