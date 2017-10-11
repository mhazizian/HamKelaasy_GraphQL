import graphene
import core.services as services
from core import HamkelaasyError, Error_code

from core.graphql_query import MessageType


class Delete_post_input(graphene.InputObjectType):
    post_id = graphene.Int(required=True)


class Delete_post(graphene.Mutation):
    class Arguments:
        data = Delete_post_input(required=True)

    Output = MessageType

    def mutate(self, info, data):
        return Delete_post.delete(info, data)

    @staticmethod
    def delete(info, data):
        if not info.context.user.is_authenticated:
            raise HamkelaasyError(Error_code.Authentication.User_not_authenticated)
        user = info.context.user.person

        services.delete_post(
            user=user,
            post_id=data.post_id,
        )
        return MessageType(type='success', message='comment deleted.')
