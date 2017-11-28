import graphene
import core.services as services
from core.models import PARENT_KEY_WORD


class PersonType(graphene.ObjectType):
    name = "person"

    # only if neccessary...
    id = graphene.Int()
    first_name = graphene.String()
    last_name = graphene.String()
    email = graphene.String()
    pic = graphene.String()
    signup_completed = graphene.Boolean()
    type = graphene.String()

    new_notification_count = graphene.Int()

    # TODO : remove these two after some weak
    has_new_password = graphene.Boolean()
    has_phone_number = graphene.Boolean()
    # for test only:
    username = graphene.String()

    childes = graphene.List(
        'core.graphql_query.StudentType',
        page_size=graphene.Int(default_value=services.DEFAULT_PAGE_SIZE),
        page=graphene.Int(default_value=1),
        kelaas_id=graphene.Int(description="privdes childern of a spacific kelaas"
                                           "(now, it only works if query is requested by a teacher)"
                                           "(only can be used if requested person in Parent)")
    )
    child = graphene.Field(
        'core.graphql_query.StudentType',
        id=graphene.Int(required=True),
        description="(only can be used if requested person in Parent)",
    )

    def resolve_childes(self, info, page, page_size, **kwargs):
        user = info.context.user.person
        if self.type == PARENT_KEY_WORD:
            query_set = services.get_parent_childes(self.parent, user, **kwargs)
            return services.apply_pagination(query_set, page=page, page_size=page_size)

    def resolve_child(self, info, id):
        user = info.context.user.person
        if self.type == PARENT_KEY_WORD:
            return services.get_parent_child(self.parent, user, id)

    def resolve_username(self, info):
        if self.user:
            return self.user.username

    def resolve_has_phone_number(self, info):
        if self.phone_number == '':
            return False
        return True

    def resolve_has_mew_password(self, info):
        if self.has_new_password:
            return True
        return False

    def resolve_new_notification_count(self, info):
        user = info.context.user.person

        return services.get_not_seen_notification_count(user, person=self)
