import graphene
from django.db.models import Count

from core import myGraphQLError

from core.graphql_query import CertificateType
from core.models import Conversation, Person, Kelaas, Certificate


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

        # TODO permission check!!
        # TODO duplicate certificate?

        if not info.context.user.is_authenticated:
            raise myGraphQLError('user not authenticated', status=401)
        user = info.context.user.person

        if user.created_certificates.filter(title=data.title).exists():
            raise myGraphQLError('duplicate certificate', status=400)

        certificate = Certificate(
            title=data.title,
            description=data.description,
            creator=user
        )
        certificate.save()
        return certificate