import graphene


class ConversationMessage(graphene.ObjectType):
    body = graphene.String()
    owner = graphene.Field('core.graphql_query.PerosnType')

    is_my_message = graphene.Boolean()

    shamsi_date = graphene.String()
    time_passed = graphene.String()

    def resolve_is_my_message(self, info):
        user = info.context.user.person

        if user.id == self.owner.id:
            return True
        return False
