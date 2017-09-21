import graphene
import core.services as services
from core import myGraphQLError

from core.graphql_query import KelaasType


class Kelaas_input(graphene.InputObjectType):
    title = graphene.String(required=True)
    description = graphene.String(default_value="")
    tags = graphene.String(description="a string of tag's id,\n\n example: '1,10,4,3,'", default_value="")


class Create_kelaas(graphene.Mutation):
    class Arguments:
        data = Kelaas_input(required=True)

    Output = KelaasType

    def mutate(self, info, data):
        return Create_kelaas.make_kelaas(info, data)

    @staticmethod
    def make_kelaas(info, data):
        if not info.context.user.is_authenticated:
            raise myGraphQLError('user not authenticated', status=401)
        user = info.context.user.person

        return services.create_kelaas(
            user=user,
            title=data.title,
            description=data.description,
            tags=data.tags
        )
