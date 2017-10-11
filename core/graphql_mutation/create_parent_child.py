import graphene
from core import HamkelaasyError, Error_code
import core.services as services

from core.graphql_query import StudentType


class Create_parent_child_input(graphene.InputObjectType):
    first_name = graphene.String(required=True)
    last_name = graphene.String(required=True)
    gender = graphene.Int(required=True)
    age = graphene.Int(required=True)


class Create_parent_child(graphene.Mutation):
    class Arguments:
        data = Create_parent_child_input(required=True)

    Output = StudentType

    def mutate(self, info, data):
        return Create_parent_child.add(info, data)

    @staticmethod
    def add(info, data):
        if not info.context.user.is_authenticated:
            raise HamkelaasyError(Error_code.Authentication.User_not_authenticated)
        user = info.context.user.person

        return services.create_parent_child(
            user=user,
            first_name=data.first_name,
            last_name=data.last_name,
            gender=data.gender,
            age=data.age,
        )
