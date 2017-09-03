import graphene


class PersonType(graphene.ObjectType):
    name = "person"

    id = graphene.Int()
    first_name = graphene.String()
    last_name = graphene.String()
    email = graphene.String()
    pic = graphene.String()
    signup_completed = graphene.Boolean()
    type = graphene.String()

    username = graphene.String()

    def resolve_username(student, info):
        return student.user.username