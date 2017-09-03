import graphene

from core.models import TEACHER_KEY_WORD
from core.graphql_utilz import PersonType


class StudentType(PersonType):
    name = "student"

    age = graphene.Int()
    parent_code = graphene.String()
    nickname = graphene.String()

    kelaases = graphene.List('core.graphql_utilz.KelaasType')
    parent = graphene.Field('core.graphql_utilz.ParentType')

    def resolve_kelaases(self, info):
        user = info.context.user.person

        if user.type == "teacher":
            return [kelaas for kelaas in self.kelaas_set.all() if user.teacher.kelasses.filter(id=kelaas.id).exists()]
        if user.type == "parent":
            return self.kelaas_set.all()

    def resolve_parent(self, info):
        user = info.context.user.person

        if user.type == TEACHER_KEY_WORD:
            for kelaas in user.teacher.kelasses.all():
                if kelaas.students.filter(pk=self.id).exists():
                    return kelaas.students.get(pk=self.id).parents