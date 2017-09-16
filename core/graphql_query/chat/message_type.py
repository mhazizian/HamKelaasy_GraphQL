import graphene


class ConversationMessageType(graphene.ObjectType):
    body = graphene.String()
    writer = graphene.Field('core.graphql_query.PersonType')

    is_my_message = graphene.Boolean()

    shamsi_date = graphene.String()
    time_passed = graphene.String()

    def resolve_is_my_message(self, info):
        user = info.context.user.person

        if user.id == self.writer.id:
            return True
        return False
