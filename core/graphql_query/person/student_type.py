import graphene
from graphql import GraphQLError

from core.models import TEACHER_KEY_WORD, STUDENT_KEY_WORD, PARENT_KEY_WORD
from core.graphql_query.utilz import it_is_him
from core.graphql_query.person import PersonType

from core.graphql_query.certificate import PersonCertificateType


class StudentType(PersonType):
    name = "student"

    age = graphene.Int()
    parent_code = graphene.String()
    nickname = graphene.String()

    kelaases = graphene.List('core.graphql_query.KelaasType')
    parent = graphene.Field('core.graphql_query.ParentType')
    certificates = graphene.List(PersonCertificateType)

    def resolve_kelaases(self, info):
        user = info.context.user.person

        if user.type == TEACHER_KEY_WORD:
            return [kelaas for kelaas in self.kelaas_set.all() if user.teacher.kelaases.filter(id=kelaas.id).exists()]
        if user.type == PARENT_KEY_WORD:
            if it_is_him(user, self.parents):
                return self.kelaas_set.all()
        if it_is_him(user, self):
            return self.kelaas_set.all()

        raise GraphQLError('Permission denied')

    def resolve_parent(self, info):
        user = info.context.user.person

        if user.type == TEACHER_KEY_WORD:
            for kelaas in user.teacher.kelaases.all():
                if kelaas.students.filter(pk=self.id).exists():
                    return self.parents

        if it_is_him(user, self):
            return self.parents
        raise GraphQLError('Permission denied')

    def resolve_certificates(self, info):
        # user = info.context.user.person ?!!!
        # what to do, what not to do?!!!
        # permission check
        res = {}

        for c_link in self.certificates.all():
            if not c_link.certificate_level.type.id in res:
                res[c_link.certificate_level.type.id] = []

            res[c_link.certificate_level.type.id].append(c_link)

        print res[1][0].certificate_level.type.creator

        return [PersonCertificateType(
            id=res[key][0].certificate_level.type.id,
            title=res[key][0].certificate_level.type.title,
            description=res[key][0].certificate_level.type.description,
            # pic=res[key][0].type.pic,
            creator=res[key][0].certificate_level.type.creator,
            levels=res[key]
        ) for key in res]
