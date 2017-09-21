import graphene
import core.services as services
from core import myGraphQLError

from core.graphql_query import ConversationType


class Create_convesation_input(graphene.InputObjectType):
    members_id = graphene.String(
        required=True,
        description="a string of member id.\n\nexample: '1,2,10,4'\n\n"
                    "by default: current user is joined this conversation "
    )
    kelaas_id = graphene.Int(requierd=True)


class Create_convesation(graphene.Mutation):
    class Arguments:
        data = Create_convesation_input(required=True)

    Output = ConversationType

    def mutate(self, info, data):
        return Create_convesation.create(info, data)

    @staticmethod
    def create(info, data):
        if not info.context.user.is_authenticated:
            raise myGraphQLError('user not authenticated', status=401)
        user = info.context.user.person

        return services.create_conversation(
            user=user,
            kelaas_id=data.kelaas_id,
            members_id=data.members_id
        )
