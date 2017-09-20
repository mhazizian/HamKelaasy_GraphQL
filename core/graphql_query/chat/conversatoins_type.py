import graphene

from core.services import DEFAULT_PAGE_SIZE


class ConversationType(graphene.ObjectType):
    name = "conversation"

    id = graphene.Int()
    messages = graphene.List(
        'core.graphql_query.ConversationMessageType',
        page_size=graphene.Int(),
        page=graphene.Int(),
    )
    last_message = graphene.Field('core.graphql_query.ConversationMessageType')
    members = graphene.List('core.graphql_query.PersonType')
    member_count = graphene.Int()
    message_count = graphene.Int()

    def resolve_messages(self, info, **kwargs):
        page_size = kwargs.get('page_size', DEFAULT_PAGE_SIZE)
        offset = kwargs.get('page', 1) * page_size

        return self.messages.all().order_by('-id')[offset - page_size:offset]

    def resolve_last_message(self, info):
        return self.messages.all().last()

    def resolve_members(self, info):
        return self.members.all()
