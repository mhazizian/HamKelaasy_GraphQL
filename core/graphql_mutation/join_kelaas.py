import graphene
import core.services as services
from core import HamkelaasyError

from core.graphql_query import KelaasType


class Join_kelaas_input(graphene.InputObjectType):
    invite_code = graphene.String(required=True)


class Join_kelaas(graphene.Mutation):
    class Arguments:
        data = Join_kelaas_input(required=True)

    Output = KelaasType

    def mutate(self, info, data):
        return Join_kelaas.join(info, data)

    @staticmethod
    def join(info, data):
        if not info.context.user.is_authenticated:
            raise HamkelaasyError('user not authenticated', status=401)
        user = info.context.user.person

        return services.join_kelaas(user=user, invite_code=data.invite_code)
