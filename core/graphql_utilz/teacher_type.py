import graphene

class TeacherType(graphene.ObjectType):
    name = "teacher"
    description = "..."

    person = graphene.Field('core.graphql_utilz.PersonType')

    kelasses = graphene.List('....')

    def resolve_kelasses(teacher, args, context, info):
        return teacher.kelasses.all()

    def resolve_person(teacher, info):
        return teacher.person
