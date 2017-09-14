from graphql import GraphQLError


class myGraphQLError(GraphQLError):
    def __init__(self, message, status=400, detail=''):
        super(myGraphQLError, self).__init__(message)
        self.message = message
        self.status = status
        self.detail = detail
