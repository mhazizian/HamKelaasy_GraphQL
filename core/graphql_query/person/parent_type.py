import graphene

from core.graphql_query.person import PersonType
import core.services as services


class ParentType(PersonType):
    name = "parent"
