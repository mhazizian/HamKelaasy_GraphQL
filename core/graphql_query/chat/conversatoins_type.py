import graphene

import core.services as services


class ConversationType(graphene.ObjectType):
    name = "conversation"

    id = graphene.Int()
    messages = graphene.List(
        'core.graphql_query.ConversationMessageType',
        page_size=graphene.Int(default_value=services.DEFAULT_PAGE_SIZE),
        page=graphene.Int(default_value=1),
    )
    last_message = graphene.Field('core.graphql_query.ConversationMessageType')
    members = graphene.List('core.graphql_query.PersonType')
    member_count = graphene.Int()
    message_count = graphene.Int()

    def resolve_messages(self, info, page, page_size):
        user = info.context.user.person

        query_set = services.conversation__get_messages(conversation=self, user=user)
        return services.apply_pagination(query_set, page=page, page_size=page_size)

    def resolve_last_message(self, info):
        return self.messages.all().last()

    def resolve_members(self, info):
        user = info.context.user.person

        queryset = self.members.exclude(id=user.id)
        return [user].extend(queryset)
