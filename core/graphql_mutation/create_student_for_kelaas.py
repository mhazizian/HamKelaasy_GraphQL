import graphene
from core import HamkelaasyError
import core.services as services

from core.graphql_query import StudentType


class Create_student_for_kelaas_input(graphene.InputObjectType):
    first_name = graphene.String(required=True)
    last_name = graphene.String(required=True)
    gender = graphene.Int(required=True)
    age = graphene.Int(required=True)
    kelaas_id = graphene.Int(required=True)


class Create_student_for_kelaas(graphene.Mutation):
    class Arguments:
        data = Create_student_for_kelaas_input(required=True)

    Output = StudentType

    def mutate(self, info, data):
        return Create_student_for_kelaas.add(info, data)

    @staticmethod
    def add(info, data):
        if not info.context.user.is_authenticated:
            raise HamkelaasyError(4011)
        user = info.context.user.person

        return services.create_student_for_kelaas(
            user=user,
            first_name=data.first_name,
            last_name=data.last_name,
            gender=data.gender,
            age=data.age,
            kelaas_id=data.kelaas_id,
        )
