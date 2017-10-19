import graphene


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
