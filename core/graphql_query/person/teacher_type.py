import graphene

from core.graphql_query.utilz import DEFAULT_PAGE_SIZE, apply_pagination
from core.graphql_query.person import PersonType


class TeacherType(PersonType):
    name = "teacher"

    kelaases = graphene.List(
        'core.graphql_query.KelaasType',
        page_size=graphene.Int(),
        page=graphene.Int(),
    )
    kelaas = graphene.Field(
        'core.graphql_query.KelaasType',
        id=graphene.Int(required=True)
    )

    def resolve_kelaas(self, info, id):
        user = info.context.user.person

        return self.get_kelaas(user, id)

    def resolve_kelaases(self, info, **kwargs):
        user = info.context.user.person

        page_size = kwargs.get('page_size', DEFAULT_PAGE_SIZE)
        offset = kwargs.get('page', 1) * page_size

        return apply_pagination(self.get_kelaases(user), page_size=page_size, page=offset)
