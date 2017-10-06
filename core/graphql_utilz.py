import six
from graphql import GraphQLError

from core import errors
from graphql.error import format_error as format_graphql_error


class HamkelaasyError(Exception):
    def __init__(self, message_code):
        self.message_code = message_code

        self.message = errors[message_code].get('message', '')
        self.status = errors[message_code].get('status', 400)


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
    if isinstance(error, GraphQLError):
        return format_graphql_error(error)

    return {'message': six.text_type(error)}
