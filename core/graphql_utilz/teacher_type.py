import graphene

class TeacherType(graphene.ObjectType):
    name = "teacher"
    description = "..."

    id = graphene.Int()
    first_name = graphene.String()
    last_name = graphene.String()
    email = graphene.String()
    pic = graphene.String()
    signup_completed = graphene.Boolean()

    user = graphene.Field('core.graphql_utilz.UserType')
    kelasses = graphene.List('....')

    def resolve_user(teacher, args, context, info):
        return teacher.user

    def resolve_kelasses(teacher, args, context, info):
        return teacher.kelasses.all()