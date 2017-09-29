import graphene
import core.services as services


class CommentType(graphene.ObjectType):
    name = "comment"

    id = graphene.Int()
    body = graphene.String()
    time_passed = graphene.String()
    owner = graphene.Field('core.graphql_query.PersonType')
    is_my_comment = graphene.Boolean()

    def resolve_owner(self, info):
        return self.owner

    def resolve_is_my_comment(self, info):
        user = info.context.user.person

        return services.is_my_comment(user=user, comment=self)
