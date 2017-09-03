import graphene

from core.models import Kelaas


class StudentType(graphene.ObjectType):
    name = "student"
    description = "..."

    id = graphene.Int()
    first_name = graphene.String()
    last_name = graphene.String()
    email = graphene.String()
    pic = graphene.String()
    signup_completed = graphene.Boolean()

    age = graphene.Int()
    parent_code = graphene.String()
    nickname = graphene.String()

    username = graphene.String()

    kelaases = graphene.List('core.graphql_utilz.KelaasType')

    def resolve_kelaases(student, info):
        return student.kelaas_set.all()

    def resolve_username(student, info):
        return student.user.username