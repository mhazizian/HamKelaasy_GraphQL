import graphene


class PersonType(graphene.ObjectType):
    name = "person"
    description = "..."

    id = graphene.Int()
    first_name = graphene.String()
    last_name = graphene.String()
    email = graphene.String()
    pic = graphene.String()
    signup_completed = graphene.Boolean()
