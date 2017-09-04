from graphql import GraphQLError


def it_is_him(obj1, obj2):
    if not obj1.id == obj2.id:
        raise GraphQLError('Permission denied')
    return True