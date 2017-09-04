import graphene
from graphql import GraphQLError

from core.graphql_utilz.utilz import it_is_him
from core.graphql_utilz.person import PersonType
from core.models import PARENT_KEY_WORD


class ParentType(PersonType):
    name = "parent"

    person = graphene.Field('core.graphql_utilz.PersonType')
    students = graphene.List('core.graphql_utilz.StudentType')

    def resolve_students(self, info):
        user = info.context.user.person

        if it_is_him(self, user):
            return self.students.all()

        raise GraphQLError('Permission denied')
