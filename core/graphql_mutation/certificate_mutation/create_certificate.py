import graphene
import core.services as services

from core import HamkelaasyError

from core.graphql_query import CertificateType


class Create_certificate_input(graphene.InputObjectType):
    title = graphene.String(required=True)
    description = graphene.String(requierd=True)


class Create_certificate(graphene.Mutation):
    class Arguments:
        data = Create_certificate_input(required=True)

    Output = CertificateType

    def mutate(self, info, data):
        return Create_certificate.create(info, data)

    @staticmethod
    def create(info, data):
        if not info.context.user.is_authenticated:
            raise HamkelaasyError(4011)
        user = info.context.user.person

        return services.create_certificate(
            user=user,
            title=data.title,
            description=data.description,
        )
