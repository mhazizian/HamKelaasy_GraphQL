import graphene
from graphql import GraphQLError

from core.graphql_query.utilz import it_is_him
from core.graphql_query.person import PersonType
from core.models import PARENT_KEY_WORD


class ParentType(PersonType):
    name = "parent"

    childes = graphene.List('core.graphql_query.StudentType')

    def resolve_childs(self, info):
        user = info.context.user.person

        if it_is_him(self, user):
            return self.childes.all()

        raise GraphQLError('Permission denied')
