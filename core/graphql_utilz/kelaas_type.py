import graphene


class KelaasType(graphene.ObjectType):
    name = "kelaas"

    id = graphene.Int()
    title = graphene.String()
    shamsi_date = graphene.String()
    description = graphene.String()
    invite_code = graphene.String()

    students = graphene.List('core.graphql_utilz.StudentType')
    tags = graphene.List('core.graphql_utilz.TagType')

    def resolve_tags(kelaas,info):
            return kelaas.tags.all()

    def resolve_students(kelaas, info):
        user = info.context.user.person

        if user.type == "teacher":
            return kelaas.students.all()
        if user.type == "parent":
            return [student for student in kelaas.students.all() if student.parents.id == user.parent.id]


