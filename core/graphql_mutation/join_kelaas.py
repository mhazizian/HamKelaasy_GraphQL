import graphene
from core import myGraphQLError

from core.graphql_query import MessageType
from core.models import STUDENT_KEY_WORD, Kelaas


class Join_kelaas_input(graphene.InputObjectType):
    invite_code = graphene.String(required=True)


class Join_kelaas(graphene.Mutation):
    class Arguments:
        data = Join_kelaas_input(required=True)

    Output = MessageType

    def mutate(self, info, data):
        if info.context.user.is_authenticated:
            if Join_kelaas.join(info, data):
                return MessageType(type="success", message="badge_count")
            raise myGraphQLError('Bad data input')

        raise myGraphQLError('Permission denied')

    @staticmethod
    def join(info, data):
        user = info.context.user.person
        if not user.type == STUDENT_KEY_WORD:
            return False

        if not Kelaas.objects.filter(invite_code=data.invite_code).exists():
            return False
        kelaas = Kelaas.objects.get(invite_code=data.invite_code)
        if not kelaas.students.filter(pk=user.id).exists():
            kelaas.students.add(user.student)

        return True
