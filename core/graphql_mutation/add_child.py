import graphene
from core import myGraphQLError

from core.graphql_query import MessageType
from core.models import PARENT_KEY_WORD, Student


class Add_child_input(graphene.InputObjectType):
    child_code = graphene.String(required=True)


class Add_child(graphene.Mutation):
    class Arguments:
        data = Add_child_input(required=True)

    Output = MessageType

    def mutate(self, info, data):
        if info.context.user.is_authenticated:
            if Add_child.add(info, data):
                return MessageType(type="success", message="child added.")
            raise myGraphQLError('Bad data input')

        raise myGraphQLError('Permission denied')
    # TODO catch exeptions and convert in to message type

    @staticmethod
    def add(info, data):
        user = info.context.user.person
        if not user.type == PARENT_KEY_WORD:
            return False

        if not Student.objects.filter(parent_code=data.child_code).exists():
            raise myGraphQLError('Permission denied')
        student = Student.objects.get(parent_code=data.child_code)
        if student.parents:
            raise myGraphQLError('Permission denied')

        student.parents = user.parent
        student.save()
        return True
