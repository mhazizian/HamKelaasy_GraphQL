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

    def resolve_tags(kelaas, args, context, info):
            return kelaas.tags.all()

    def resolve_students(kelaas, args, context, info):
        return kelaas.students.all()


