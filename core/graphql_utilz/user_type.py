import graphene


class UserType(graphene.ObjectType):
    name = "user"
    description = "..."

    id = graphene.Int()
    username = graphene.String()