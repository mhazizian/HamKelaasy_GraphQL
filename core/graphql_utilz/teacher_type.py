import graphene

from core.graphql_utilz import PersonType


class TeacherType(PersonType):
    name = "teacher"

    kelasses = graphene.List('....')

    def resolve_kelasses(self, info):
        return self.kelasses.all()
