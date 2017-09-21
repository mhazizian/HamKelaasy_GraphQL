import graphene
from core import myGraphQLError
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
            raise myGraphQLError('user not authenticated', status=401)
        user = info.context.user.person

        return services.add_child(user=user, child_code=data.child_code)
