import graphene
from core import myGraphQLError

from core.graphql_query import MessageType
from core.models import Conversation, Conversation_message


class Send_message_input(graphene.InputObjectType):
    conversation_id = graphene.Int(required=True)
    message = graphene.String(required=True)


class Send_message(graphene.Mutation):
    class Arguments:
        data = Send_message_input(required=True)

    Output = MessageType

    def mutate(self, info, data):
        if Send_message.send_message(info, data):
            return MessageType(type="success", message="message added")

    @staticmethod
    def send_message(info, data):
        if not info.context.user.is_authenticated:
            raise myGraphQLError('user not authenticated', status=401)
        user = info.context.user.person

        try:
            conversation = Conversation.objects.get(pk=data.conversation_id)
        except Conversation.DoesNotExist:
            raise myGraphQLError('Convesation not found', status=404)

        if not conversation.members.filter(pk=user.id).exists():
            raise myGraphQLError('Permission denied', status=403)

        msg = Conversation_message(
            writer=user,
            body=data.message,
            conversation_id=data.conversation_id
        )
        msg.save()
        return True
