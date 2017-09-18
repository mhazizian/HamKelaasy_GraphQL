import six
from graphql import GraphQLError
from graphql.error import format_error as format_graphql_error


class myGraphQLError(GraphQLError):
    def __init__(self, message, status=400, detail=''):
        super(myGraphQLError, self).__init__(message)
        self.message = message
        self.status = status
        self.detail = detail


def get_status_code(response):
    if response.errors:
        status_code = 400
        if hasattr(response.errors[0], 'original_error'):
            if isinstance(response.errors[0].original_error, myGraphQLError):
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
