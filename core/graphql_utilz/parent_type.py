import graphene
from core.graphql_utilz import PersonType


class ParentType(PersonType):
    name = "parent"

    person = graphene.Field('core.graphql_utilz.PersonType')
    students = graphene.List('core.graphql_utilz.StudentType')

    def resolve_students(self, info):
        return self.students.all()
        # permission check
