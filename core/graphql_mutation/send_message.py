import graphene
import core.services as services

from core import HamkelaasyError, Error_code
from core.graphql_query import ConversationMessageType


class Send_message_input(graphene.InputObjectType):
    conversation_id = graphene.Int(required=True)
    message = graphene.String(required=True)


class Send_message(graphene.Mutation):
    class Arguments:
        data = Send_message_input(required=True)

    Output = ConversationMessageType

    def mutate(self, info, data):
        return Send_message.send_message(info, data)

    @staticmethod
    def send_message(info, data):
        if not info.context.user.is_authenticated:
            raise HamkelaasyError(Error_code.Authentication.User_not_authenticated)
        user = info.context.user.person

        return services.send_message(
            user=user,
            conversation_id=data.conversation_id,
            message=data.message
        )
