import graphene

from core.graphql_query import DEFAULT_PAGE_SIZE


class ConversationType(graphene.ObjectType):
    name = "conversation"

    messages = graphene.List(
        'core.graphql_query.ConversationMessageType',
        page_size=graphene.Int(),
        page=graphene.Int(),
    )
    member_count = graphene.Int()
    message_count = graphene.Int()

    def resolve_messages(self, info, **kwargs):
        page_size = kwargs.get('page_size', DEFAULT_PAGE_SIZE)
        offset = kwargs.get('page', 1) * page_size

        return self.messages.all().order_by('-id')[offset - page_size:offset]
