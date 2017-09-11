import graphene
from graphql import GraphQLError

from core.graphql_query.utilz import it_is_him, DEFAULT_PAGE_SIZE
from core.graphql_query.person import PersonType
from core.models import TEACHER_KEY_WORD


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

        if it_is_him(self, user):
            if user.teacher.kelaases.filter(pk=id).exists():
                return self.kelaases.get(pk=id)
        raise GraphQLError('Permission denied')

    def resolve_kelaases(self, info, **kwargs):
        user = info.context.user.person

        page_size = kwargs.get('page_size', DEFAULT_PAGE_SIZE)
        offset = kwargs.get('page', 1) * page_size

        if it_is_him(self, user):
            if offset == page_size:
                return self.kelaases.all()[-offset:][::-1]
            return self.kelaases.all()[-offset:-offset + page_size][::-1]
        raise GraphQLError('Permission denied')
