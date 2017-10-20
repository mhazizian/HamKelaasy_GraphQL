import graphene
import core.services as services


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
