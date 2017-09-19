import graphene
from core import myGraphQLError

from core.graphql_query.utilz import it_is_him, DEFAULT_PAGE_SIZE, apply_pagination
from core.graphql_query.person import PersonType
from core.models import PARENT_KEY_WORD, Parent


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

        return apply_pagination(self.get_childes(user), page=offset, page_size=page_size)

    def resolve_child(self, info, id):
        user = info.context.user.person
        return self.get_child(user, id)
