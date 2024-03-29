import graphene
import core.services as services
from core import HamkelaasyError, Error_code

from core.graphql_query import MessageType


class Delete_comment_input(graphene.InputObjectType):
    comment_id = graphene.Int(required=True)


class Delete_comment(graphene.Mutation):
    class Arguments:
        data = Delete_comment_input(required=True)

    Output = MessageType

    def mutate(self, info, data):
        return Delete_comment.delete(info, data)

    @staticmethod
    def delete(info, data):
        if not info.context.user.is_authenticated:
            raise HamkelaasyError(Error_code.Authentication.User_not_authenticated)
        user = info.context.user.person

        services.delete_comment(
            user=user,
            comment_id=data.comment_id,
        )
        return MessageType(type='success', message='comment deleted.')
