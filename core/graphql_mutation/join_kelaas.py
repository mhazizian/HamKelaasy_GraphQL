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
        if Join_kelaas.join(info, data):
            return MessageType(type="success", message="badge_count")

    @staticmethod
    def join(info, data):
        if not info.context.user.is_authenticated:
            raise myGraphQLError('user not authenticated', status=401)
        user = info.context.user.person

        if not user.type == STUDENT_KEY_WORD:
            raise myGraphQLError('Permission denied', status=403)

        try:
            kelaas = Kelaas.objects.get(invite_code=data.invite_code)
        except Kelaas.DoesNotExist:
            raise myGraphQLError('Kelaas not found', status=404)

        if not kelaas.students.filter(pk=user.id).exists():
            kelaas.students.add(user.student)
            kelaas.save()
        return True
