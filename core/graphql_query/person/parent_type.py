import graphene

from core.graphql_query.person import PersonType
from core.services import DEFAULT_PAGE_SIZE, apply_pagination, parent__get_childes, parent__get_child


class ParentType(PersonType):
    name = "parent"

    childes = graphene.List(
        'core.graphql_query.StudentType',
        page_size=graphene.Int(),
        page=graphene.Int(),
    )
    child = graphene.Field(
        'core.graphql_query.StudentType',
        id=graphene.Int(required=True)
    )

    def resolve_childes(self, info, **kwargs):
        user = info.context.user.person

        page_size = kwargs.get('page_size', DEFAULT_PAGE_SIZE)
        offset = kwargs.get('page', 1) * page_size

        return apply_pagination(parent__get_childes(self, user), page=offset, page_size=page_size)

    def resolve_child(self, info, id):
        user = info.context.user.person
        return parent__get_child(self, user, id)
