import graphene

from core.graphql_query.person import PersonType
import core.services as services


class TeacherType(PersonType):
    name = "teacher"

    kelaases = graphene.List(
        'core.graphql_query.KelaasType',
        page_size=graphene.Int(default_value=services.DEFAULT_PAGE_SIZE),
        page=graphene.Int(default_value=1),
    )
    kelaas = graphene.Field(
        'core.graphql_query.KelaasType',
        id=graphene.Int(required=True)
    )

    def resolve_kelaas(self, info, id):
        user = info.context.user.person

        return services.teacher__get_kelaas(self, user, id)

    def resolve_kelaases(self, info, page_size, page):
        user = info.context.user.person

        query_set = services.teacher__get_kelaases(self, user)
        return services.apply_pagination(query_set, page_size=page_size, page=page)
