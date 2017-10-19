# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import jdatetime as jdatetime

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
        self.message = errors[error_code.value].get('message', '')
        self.status = errors[error_code.value].get('status', 400)

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
        logger.exception(
            '\n\nbegin >=============================================\n'
            + '>>> HamKelaasyError:\n' + self.message
        )

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


# ____________________________________________________________________________________
# ____________________________________________________________________________________

def to_shamsi_date(time):
    year, month, day = jdatetime.GregorianToJalali(time.year, time.month, time.day).getJalaliList()
    return jdatetime.datetime(year, month, day, time.hour, time.minute, time.second).strftime("%a, %d %b %Y %H:%M")


def pretty_past_time(diff):
    """
    Get a delta  datetime object and return a
    pretty string like 'an hour ago', 'Yesterday', '3 months ago',
    'just now', etc
    """
    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return ''

    if day_diff == 0:
        if second_diff < 10:
            return "همین الان"
        if second_diff < 60:
            return str(second_diff) + " ثانیه پیش"
        if second_diff < 120:
            return "یک دقیقه پیش"
        if second_diff < 3600:
            return str(second_diff / 60) + " دقیقه پیش"
        if second_diff < 7200:
            return "یک ساعت پیش"
        if second_diff < 86400:
            return str(second_diff / 3600) + " ساعت پیش"
    if day_diff == 1:
        return "دیروز"
    if day_diff < 7:
        return str(day_diff) + " روز پیش"
    if day_diff < 31:
        return str(day_diff / 7) + " هفته پیش"
    if day_diff < 365:
        return str(day_diff / 30) + " ماه پیش"
    return str(day_diff / 365) + " سال پیش"


def pretty_remaining_time(diff):
    """
    Get a delta  datetime object and return a
    pretty string like 'an hour remains', '1 day', '3 months',
    'just now', etc
    """
    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return ''

    if day_diff == 0:
        if second_diff < 10:
            return "همین الان"
        if second_diff < 60:
            return str(second_diff) + " ثانیه مانده"
        if second_diff < 120:
            return "یک دقیقه مانده"
        if second_diff < 3600:
            return str(second_diff / 60) + " دقیقه مانده"
        if second_diff < 7200:
            return "یک ساعت مانده"
        if second_diff < 86400:
            return str(second_diff / 3600) + " ساعت مانده"
    if day_diff == 1:
        return "فردا"
    if day_diff < 7:
        return str(day_diff) + " روز مانده"
    if day_diff < 31:
        return str(day_diff / 7) + " هفته مانده"
    if day_diff < 365:
        return str(day_diff / 30) + " ماه مانده"
    return str(day_diff / 365) + " سال مانده"
