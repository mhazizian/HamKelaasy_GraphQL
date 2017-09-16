import graphene
from core import myGraphQLError

from core.graphql_query import StudentType
from core.models import PARENT_KEY_WORD, Student


class Add_child_input(graphene.InputObjectType):
    child_code = graphene.String(required=True)


class Add_child(graphene.Mutation):
    class Arguments:
        data = Add_child_input(required=True)

    Output = StudentType

    def mutate(self, info, data):
        return Add_child.add(info, data)

    @staticmethod
    def add(info, data):
        if not info.context.user.is_authenticated:
            raise myGraphQLError('user not authenticated', status=401)
        user = info.context.user.person

        if not user.type == PARENT_KEY_WORD:
            raise myGraphQLError('Permission denied', status=403)

        try:
            student = Student.objects.get(parent_code=data.child_code)
            if student.parents:
                raise myGraphQLError('Permission denied', status=403)

            student.parents = user.parent
            student.save()
        except Student.DoesNotExist:
            raise myGraphQLError('Student not found', status=404)
        return student
