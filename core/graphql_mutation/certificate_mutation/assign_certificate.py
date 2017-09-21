import graphene
import core.services as services
from core import myGraphQLError

from core.graphql_query import CertificateLinkType


class Assign_certificate_input(graphene.InputObjectType):
    owner_id = graphene.Int(required=True, description="in most cases, student_id")
    type_id = graphene.Int(required=True, description="certificate type id")
    level = graphene.Int(required=True)


class Assign_certificate(graphene.Mutation):
    class Arguments:
        data = Assign_certificate_input(required=True)

    Output = CertificateLinkType

    def mutate(self, info, data):
        return Assign_certificate.assign(info, data)

    @staticmethod
    def assign(info, data):
        if not info.context.user.is_authenticated:
            raise myGraphQLError('user not authenticated', status=401)
        user = info.context.user.person

        return services.assign_certificate(
            user=user,
            owner_id=data.owner_id,
            level=data.level,
            type_id=data.type_id,
        )
