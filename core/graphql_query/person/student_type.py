import exceptions
import graphene
from core import myGraphQLError

from core.models import TEACHER_KEY_WORD, STUDENT_KEY_WORD, PARENT_KEY_WORD, Kelaas
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
    kelaas = graphene.Field(
        'core.graphql_query.KelaasType',
        id=graphene.Int(),
    )
    parent = graphene.Field('core.graphql_query.ParentType')
    badges = graphene.List(
        'core.graphql_query.BadgeLink',
        kelaas_id=graphene.Int(description="Optional.\n\n if provided, only shows badges from this kelaas"),
        page_size=graphene.Int(),
        page=graphene.Int(),
    )
    certificates = graphene.List(PersonCertificateType)
    tasks = graphene.List(
        'core.graphql_query.TaskType',
        kelaas_id=graphene.Int(description="Optional.\n\n if provided, only shows badges from this kelaas"),
        page_size=graphene.Int(),
        page=graphene.Int(),
    )

    def resolve_kelaases(self, info, **kwargs):
        user = info.context.user.person

        page_size = kwargs.get('page_size', DEFAULT_PAGE_SIZE)
        offset = kwargs.get('page', 1) * page_size

        if user.type == TEACHER_KEY_WORD:
            return [kelaas for kelaas in self.kelaases.all() if user.teacher.kelaases.filter(id=kelaas.id).exists()].reverse()[offset - page_size:offset]

        if user.type == PARENT_KEY_WORD:
            if it_is_him(user, self.parents):
                return self.kelaases.all().order_by('-id')[offset - page_size:offset]

        if it_is_him(user, self):
            return self.kelaases.all().order_by('-id')[offset - page_size:offset]

        raise myGraphQLError('Permission denied', status=403)

    def resolve_kelaas(self, info, id):
        user = info.context.user.person

        if user.type == PARENT_KEY_WORD:
            if it_is_him(user, self.parents):
                if self.kelaases.filter(pk=id).exists():
                    return self.kelaases.get(pk=id)

        if user.type == TEACHER_KEY_WORD:
            if self.kelaases.filter(pk=id).exists():
                if user.teacher.kelaases.filter(pk=id).exists():
                    return self.kelaases.get(pk=id)

        if it_is_him(user, self):
            if self.kelaases.filter(pk=id).exists():
                return self.kelaases.get(pk=id)

        raise myGraphQLError('Permission denied', status=403)

    def resolve_parent(self, info):
        user = info.context.user.person

        if user.type == TEACHER_KEY_WORD:
            for kelaas in user.teacher.kelaases.all():
                if kelaas.students.filter(pk=self.id).exists():
                    return self.parents

        if it_is_him(user, self):
            return self.parents

        raise myGraphQLError('Permission denied', status=403)

    def resolve_badges(self, info, **kwargs):
        user = info.context.user.person

        page_size = kwargs.get('page_size', DEFAULT_PAGE_SIZE)
        offset = kwargs.get('page', 1) * page_size

        if it_is_him(user, self):
            if 'kelaas_id' in kwargs:
                return self.badges.filter(kelaas_id=kwargs['kelaas_id'])[offset - page_size:offset]
            return self.badges.all()[offset - page_size:offset]

        if user.type == TEACHER_KEY_WORD:
            if 'kelaas_id' in kwargs:
                if user.teacher.kelaases.filter(kelaas_id=kwargs['kelaas_id']).exists():
                    return self.badges.filter(kelaas_id=kwargs['kelaas_id'])[offset - page_size:offset]
            badges = []
            for kelaas in user.teacher.kelaases.all():
                if kelaas.students.filter(pk=self.id).exists():
                    badges.extend(self.badges.filter(kelaas=kelaas))
            return badges[offset - page_size:offset]

        if user.type == PARENT_KEY_WORD:
            if it_is_him(user, self.parents):
                if 'kelaas_id' in kwargs:
                    self.badges.filter(kelaas_id=kwargs['kelaas_id'])
                return self.badges.all()[offset - page_size:offset]

        raise myGraphQLError('Permission denied', status=403)

    def resolve_certificates(self, info):
        # TODO permission check
        # user = info.context.user.person ?!!!
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

    def resolve_tasks(self, info, **kwargs):
        user = info.context.user.person

        page_size = kwargs.get('page_size', DEFAULT_PAGE_SIZE)
        offset = kwargs.get('page', 1) * page_size

        if it_is_him(user, self):
            if 'kelaas_id' in kwargs:
                return self.tasks.filter(kelaas_id=kwargs['kelaas_id'], is_done=False)[offset - page_size:offset]
            return self.tasks.all(is_done=False)[offset - page_size:offset]

        if user.type == TEACHER_KEY_WORD:
            try:
                kelaas = Kelaas.objects.get(pk=kwargs['kelaas_id'])
                return self.tasks.filter(kelaas_id=kelaas.id)[offset - page_size:offset]
            except Kelaas.DoesNotExist:
                raise myGraphQLError('Kelaas not found', status=404)
            except exceptions.KeyError:
                raise myGraphQLError('"kelaas_id" is necessary', status=400)

        raise myGraphQLError('Permission denied', status=403)