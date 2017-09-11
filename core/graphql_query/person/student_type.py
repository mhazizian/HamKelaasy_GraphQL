import graphene
from graphql import GraphQLError

from core.models import TEACHER_KEY_WORD, STUDENT_KEY_WORD, PARENT_KEY_WORD
from core.graphql_query.utilz import it_is_him, DEFAULT_PAGE_SIZE
from core.graphql_query.person import PersonType

from core.graphql_query.certificate import PersonCertificateType


class StudentType(PersonType):
    name = "student"

    age = graphene.Int()
    parent_code = graphene.String()
    nickname = graphene.String()

    kelaases = graphene.List(
        'core.graphql_query.KelaasType',
        page_size=graphene.Int(),
        page=graphene.Int(),
    )
    parent = graphene.Field('core.graphql_query.ParentType')
    badges = graphene.List(
        'core.graphql_query.BadgeLink',
        kelaas_id=graphene.Int(description="Optional.\n\n if provided, only shows badges from this kelaas"),
        page_size=graphene.Int(),
        page=graphene.Int(),
    )
    certificates = graphene.List(PersonCertificateType)

    def resolve_kelaases(self, info, **kwargs):
        user = info.context.user.person

        page_size = kwargs.get('page_size', DEFAULT_PAGE_SIZE)
        offset = kwargs.get('page', 1) * page_size

        if user.type == TEACHER_KEY_WORD:
            if offset == page_size:
                return [kelaas for kelaas in self.kelaases.all() if user.teacher.kelaases.filter(id=kelaas.id).exists()][-offset:][::-1]
            return [kelaas for kelaas in self.kelaases.all() if user.teacher.kelaases.filter(id=kelaas.id).exists()][-offset:-offset + page_size][::-1]
        if user.type == PARENT_KEY_WORD:
            if it_is_him(user, self.parents):
                if offset == page_size:
                    return self.kelaases.all()[-offset:][::-1]
                return self.kelaases.all()[-offset:-offset + page_size][::-1]
        if it_is_him(user, self):
            if offset == page_size:
                return self.kelaases.all()[-offset:][::-1]
            return self.kelaases.all()[-offset:-offset + page_size][::-1]

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

    def resolve_badges(self, info, **kwargs):
        user = info.context.user.person

        page_size = kwargs.get('page_size', DEFAULT_PAGE_SIZE)
        offset = kwargs.get('page', 1) * page_size

        if it_is_him(user, self):
            if 'kelaas_id' in kwargs:
                self.badges.filter(kelaas_id=kwargs['kelaas_id'])
            return self.badges.all()[offset - page_size:offset]

        if user.type == TEACHER_KEY_WORD:
            badges = []
            for kelaas in user.teacher.kelaases.all():
                if kelaas.students.filter(pk=self.id).exists():
                    badges.append(self.badges.filter(kelaas=kelaas))
            return badges[offset - page_size:offset]

        if user.type == PARENT_KEY_WORD:
            if it_is_him(user, self.parents):
                if 'kelaas_id' in kwargs:
                    self.badges.filter(kelaas_id=kwargs['kelaas_id'])
                return self.badges.all()[offset - page_size:offset]

        raise GraphQLError('Permission denied')

    def resolve_certificates(self, info):
        # user = info.context.user.person ?!!!
        # permission check
        res = {}

        for c_link in self.certificates.all():
            if not c_link.certificate_level.type.id in res:
                res[c_link.certificate_level.type.id] = []

            res[c_link.certificate_level.type.id].append(c_link)

        return [PersonCertificateType(
            id=res[key][0].certificate_level.type.id,
            title=res[key][0].certificate_level.type.title,
            description=res[key][0].certificate_level.type.description,
            pic=res[key][0].certificate_level.type.pic,
            creator=res[key][0].certificate_level.type.creator,
            levels=res[key]
        ) for key in res]
