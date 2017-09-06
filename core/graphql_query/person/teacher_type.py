import graphene
from graphql import GraphQLError

from core.graphql_query.utilz import it_is_him
from core.graphql_query.person import PersonType
from core.models import TEACHER_KEY_WORD


class TeacherType(PersonType):
    name = "teacher"

    kelaases = graphene.List('core.graphql_query.KelaasType')
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

    def resolve_kelaases(self, info):
        user = info.context.user.person

        if it_is_him(self, user):
            return self.kelaases.all()
        raise GraphQLError('Permission denied')
