import graphene
from core import HamkelaasyError, Error_code
import core.services as services

from core.graphql_query import StudentType


class Add_child_input(graphene.InputObjectType):
    child_code = graphene.String(required=True)


class Add_child(graphene.Mutation):
    class Arguments:
        data = Add_child_input(required=True)

    Output = StudentType

    def mutate(self, info, data):
        return Add_child.add(info, data)

    @staticmethod
    def add(info, data):
        if not info.context.user.is_authenticated:
            raise HamkelaasyError(Error_code.Authentication.User_not_authenticated)
        user = info.context.user.person

        return services.add_child_by_code(user=user, child_code=data.child_code)


# ______________________________________________________________________
# ______________________________________________________________________

class Add_child_by_token_input(graphene.InputObjectType):
    child_token = graphene.String(required=True)


class Add_child_by_token(graphene.Mutation):
    class Arguments:
        data = Add_child_by_token_input(required=True)

    Output = StudentType

    def mutate(self, info, data):
        return Add_child_by_token.add(info, data)

    @staticmethod
    def add(info, data):
        if not info.context.user.is_authenticated:
            raise HamkelaasyError(Error_code.Authentication.User_not_authenticated)
        user = info.context.user.person

        return services.add_child_by_token(user=user, child_token=data.child_token)
