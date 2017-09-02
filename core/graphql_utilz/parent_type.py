import graphene


class ParentType(graphene.ObjectType):
    name = "parent"
    description = "..."

    id = graphene.Int()
    first_name = graphene.String()
    last_name = graphene.String()
    email = graphene.String()
    pic = graphene.String()
    signup_completed = graphene.Boolean()

    user = graphene.Field('core.graphql_utilz.UserType')

    def resolve_user(parent, args, context, info):
        return parent.user

