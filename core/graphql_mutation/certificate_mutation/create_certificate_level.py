import graphene
import core.services as services
from core import HamkelaasyError

from core.graphql_query import CertificateLevelType


class Create_certificate_level_input(graphene.InputObjectType):
    certificate_id = graphene.Int(required=True)
    level = graphene.Int(required=True)
    level_description = graphene.String(requierd=True)


class Create_certificate_level(graphene.Mutation):
    class Arguments:
        data = Create_certificate_level_input(required=True)

    Output = CertificateLevelType

    def mutate(self, info, data):
        return Create_certificate_level.create(info, data)

    @staticmethod
    def create(info, data):
        if not info.context.user.is_authenticated:
            raise HamkelaasyError('user not authenticated', status=401)
        user = info.context.user.person

        return services.create_certificate_level(
            user=user,
            certificate_id=data.certificate_id,
            level=data.level,
            level_description=data.level_description
        )
