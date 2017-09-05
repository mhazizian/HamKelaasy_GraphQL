import graphene


class PersonType(graphene.ObjectType):
    name = "person"

    # only if neccessary...
    id = graphene.Int()
    first_name = graphene.String()
    last_name = graphene.String()
    email = graphene.String()
    pic = graphene.String()
    signup_completed = graphene.Boolean()
    type = graphene.String()

    # for test only:
    username = graphene.String()

    def resolve_username(self, info):
        return self.user.username