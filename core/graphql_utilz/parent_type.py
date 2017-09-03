import graphene


class ParentType(graphene.ObjectType):
    name = "parent"

    person = graphene.Field('core.graphql_utilz.PersonType')
    students = graphene.List('core.graphql_utilz.StudentType')

    def resolve_person(student, info):
        return student.person

    def resolve_students(parent, info):
        return parent.students.all()
        #permission check
