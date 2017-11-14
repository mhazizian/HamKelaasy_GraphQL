import graphene
import core.services as services

from core import HamkelaasyError, Error_code
from core.graphql_query import MessageType


class Remove_student_from_kelaas_input(graphene.InputObjectType):
    kelaas_id = graphene.Int(required=True)
    student_id = graphene.Int(required=True)


class Remove_student_from_kelaas(graphene.Mutation):
    class Arguments:
        data = Remove_student_from_kelaas_input(required=True)

    Output = MessageType

    def mutate(self, info, data):
        return Remove_student_from_kelaas.remove(info, data)

    @staticmethod
    def remove(info, data):
        if not info.context.user.is_authenticated:
            raise HamkelaasyError(Error_code.Authentication.User_not_authenticated)
        user = info.context.user.person

        services.remove_student_from_kelaas(
            user=user,
            kelaas_id=data.kelaas_id,
            student_id=data.student_id,
        )
        return MessageType(type='success', message='student removed from kelaas.')
