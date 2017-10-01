import graphene
import core.services as services
from core import myGraphQLError

from core.graphql_query import KelaasType


class Join_kelaas_for_parent_input(graphene.InputObjectType):
    invite_code = graphene.String(required=True)
    student_id = graphene.Int(required=True)


class Join_kelaas_for_parent(graphene.Mutation):
    class Arguments:
        data = Join_kelaas_for_parent_input(required=True)

    Output = KelaasType

    def mutate(self, info, data):
        return Join_kelaas_for_parent.join(info, data)

    @staticmethod
    def join(info, data):
        if not info.context.user.is_authenticated:
            raise myGraphQLError('user not authenticated', status=401)
        user = info.context.user.person

        return services.join_kelaas_for_parent(
            user=user,
            invite_code=data.invite_code,
            student_id=data.student_id,
        )
