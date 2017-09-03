import graphene

from core.models import Kelaas


class StudentType(graphene.ObjectType):
    name = "student"

    person = graphene.Field('core.graphql_utilz.PersonType')

    age = graphene.Int()
    parent_code = graphene.String()
    nickname = graphene.String()

    kelaases = graphene.List('core.graphql_utilz.KelaasType')

    def resolve_kelaases(student, info):
        user = info.context.user.person

        if user.type == "teacher":
            return [kelaas for kelaas in student.kelaas_set.all() if user.teacher.kelasses.filter(id=kelaas.id).exists()]
        if user.type == "parent":
            return student.kelaas_set.all()

    def resolve_person(student, info):
        return student.person