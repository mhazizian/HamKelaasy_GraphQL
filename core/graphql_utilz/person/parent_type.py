import graphene
from graphql import GraphQLError

from core.graphql_utilz import PersonType
from core.models import PARENT_KEY_WORD


class ParentType(PersonType):
    name = "parent"

    person = graphene.Field('core.graphql_utilz.PersonType')
    students = graphene.List('core.graphql_utilz.StudentType')

    def resolve_students(self, info):
        user = info.context.user.person
        if not user.id == self.id:
            raise GraphQLError('Permission denied')

        if user.type == PARENT_KEY_WORD:
            return self.students.all()

    raise GraphQLError('Permission denied')
