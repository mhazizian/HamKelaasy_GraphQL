import graphene

class StudentType(graphene.ObjectType):
    name = "student"
    description = "..."

    id = graphene.Int()
    first_name = graphene.String()
    last_name = graphene.String()
    email = graphene.String()
    pic = graphene.String()
    signup_completed = graphene.Boolean()

    age = graphene.Int()
    parent_code = graphene.String()
    nickname = graphene.String()

    user = graphene.Field('core.graphql_utilz.UserType')

    def resolve_user(student, args, context, info):
        return student.user