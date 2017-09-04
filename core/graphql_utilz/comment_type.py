import graphene


class CommentType(graphene.ObjectType):
    name = "comment"

    body = graphene.String()
    time_passed = graphene.String()
    owner = graphene.Field('core.graphql_utilz.PersonType')

    def resolve_owner(self, info):
        return self.owner
