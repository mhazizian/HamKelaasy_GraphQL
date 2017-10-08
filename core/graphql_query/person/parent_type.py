import graphene

from core.graphql_query.person import PersonType
import core.services as services


class ParentType(PersonType):
    name = "parent"

    childes = graphene.List(
        'core.graphql_query.StudentType',
        page_size=graphene.Int(default_value=services.DEFAULT_PAGE_SIZE),
        page=graphene.Int(default_value=1),
        kelaas_id=graphene.Int(description="privdes childern of a spacific kelaas"
                                           "(now, it only works if query is requested by a teacher)")
    )
    child = graphene.Field(
        'core.graphql_query.StudentType',
        id=graphene.Int(required=True)
    )

    def resolve_childes(self, info, page, page_size, **kwargs):
        user = info.context.user.person

        query_set = services.get_parent_childes(self, user, **kwargs)
        return services.apply_pagination(query_set, page=page, page_size=page_size)

    def resolve_child(self, info, id):
        user = info.context.user.person
        return services.get_parent_child(self, user, id)
