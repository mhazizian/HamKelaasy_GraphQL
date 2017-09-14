
class myGraphQLError(Exception):
    def __init__(self, message, status=400, detail=''):
        self.message = message
        self.status = status
        self.detail = detail
