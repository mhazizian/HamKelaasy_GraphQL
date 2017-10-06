import exceptions
import graphene

from core import HamkelaasyError

from core.models import TEACHER_KEY_WORD, Kelaas
from core.graphql_query.utilz import it_is_him
from core.graphql_query.person import PersonType

from core.graphql_query.certificate import PersonCertificateType
import core.services as services


class StudentType(PersonType):
    name = "student"

    age = graphene.Int()
    code = graphene.String()

    kelaases = graphene.List(
        'core.graphql_query.KelaasType',
        page_size=graphene.Int(default_value=services.DEFAULT_PAGE_SIZE),
        page=graphene.Int(default_value=1),
    )
    kelaas = graphene.Field(
        'core.graphql_query.KelaasType',
        id=graphene.Int(),
    )
    parent = graphene.Field('core.graphql_query.ParentType')
    badges = graphene.List(
        'core.graphql_query.BadgeLink',
        kelaas_id=graphene.Int(description="Optional.\n\n if provided, only shows badges from this kelaas"),
        page_size=graphene.Int(default_value=services.DEFAULT_PAGE_SIZE),
        page=graphene.Int(default_value=1),
    )
    certificates = graphene.List(PersonCertificateType)
    tasks = graphene.List(
        'core.graphql_query.TaskType',
        kelaas_id=graphene.Int(description="Optional.\n\n if provided, only shows badges from this kelaas"),
        done=graphene.Boolean(default_value=False,
                              description="if True, then only shows tasks whiches are already done\n\ndefauly: False"),
        page_size=graphene.Int(default_value=services.DEFAULT_PAGE_SIZE),
        page=graphene.Int(default_value=1),
    )

    def resolve_code(self, info):
        user = info.context.user.person
        return services.student__get_code(student=self, user=user)

    def resolve_kelaases(self, info, page, page_size):
        user = info.context.user.person

        query_set = services.student__get_kelaases(student=self, user=user)
        return services.apply_pagination(query_set, page_size=page_size, page=page)

    def resolve_kelaas(self, info, id):
        user = info.context.user.person

        return services.student__get_kelaas(student=self, user=user, kelaas_id=id)

    def resolve_parent(self, info):
        user = info.context.user.person
        return services.student__get_parent(student=self, user=user)

    def resolve_badges(self, info, page, page_size, **kwargs):
        user = info.context.user.person

        query_set = services.student__get_badges(student=self, user=user, **kwargs)
        return services.apply_pagination(query_set, page_size=page_size, page=page)

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

        page_size = kwargs.get('page_size', services.DEFAULT_PAGE_SIZE)
        offset = kwargs.get('page', 1) * page_size

        # TODO fix order of tasks, suggestion: ordered by remaning time from less to bigger
        # to do so: user annotate along with order_by
        if it_is_him(user, self):
            if 'kelaas_id' in kwargs:
                return self.tasks.filter(kelaas_id=kwargs['kelaas_id'], is_done=kwargs['done']).order_by('-id')[
                       offset - page_size:offset]
            return self.tasks.filter(is_done=kwargs['done']).order_by('-id')[offset - page_size:offset]

        if user.type == TEACHER_KEY_WORD:
            try:
                kelaas = Kelaas.objects.get(pk=kwargs['kelaas_id'])
                return self.tasks.filter(kelaas_id=kelaas.id, is_done=kwargs['done'])[offset - page_size:offset]
            except Kelaas.DoesNotExist:
                raise HamkelaasyError(4041)
            except exceptions.KeyError:
                raise HamkelaasyError(4006)

        raise HamkelaasyError(4032)
