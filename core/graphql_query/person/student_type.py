import graphene
from graphql import GraphQLError

from core.models import TEACHER_KEY_WORD, STUDENT_KEY_WORD, PARENT_KEY_WORD
from core.graphql_query.utilz import it_is_him
from core.graphql_query.person import PersonType


class StudentType(PersonType):
    name = "student"

    age = graphene.Int()
    parent_code = graphene.String()
    nickname = graphene.String()

    kelaases = graphene.List('core.graphql_query.KelaasType')
    parent = graphene.Field('core.graphql_query.ParentType')
    certificates = graphene.List('core.graphql_query.CertificateType')

    def resolve_kelaases(self, info):
        user = info.context.user.person

        if user.type == TEACHER_KEY_WORD:
            return [kelaas for kelaas in self.kelaas_set.all() if user.teacher.kelasses.filter(id=kelaas.id).exists()]
        if user.type == PARENT_KEY_WORD:
            if it_is_him(user, self.parents):
                return self.kelaas_set.all()
        if it_is_him(user, self):
            return self.kelaas_set.all()

        raise GraphQLError('Permission denied')

    def resolve_parent(self, info):
        user = info.context.user.person

        if user.type == TEACHER_KEY_WORD:
            for kelaas in user.teacher.kelasses.all():
                if kelaas.students.filter(pk=self.id).exists():
                    return self.parents

        if it_is_him(user, self):
            return self.parents
        raise GraphQLError('Permission denied')

    def resolve_certificates(self, info):
        # what to do, what not to do?!!!
        pass
