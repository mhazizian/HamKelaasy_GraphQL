import graphene

from core import myGraphQLError

from core.graphql_query import CertificateLevelType
from core.models import Certificate, Certificate_level


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
        # TODO permission check!!
        if not info.context.user.is_authenticated:
            raise myGraphQLError('user not authenticated', status=401)
        user = info.context.user.person

        try:
            certificate = Certificate.objects.get(pk=data.certificate_id)
        except Certificate.DoesNotExist:
            raise myGraphQLError('Certificate not found', status=404)


        if not user.id == certificate.creator.id:
            raise myGraphQLError('Permission denied', status=403)

        certi_level = Certificate_level(
            level=data.level,
            level_description=data.level_description,
            type=certificate,
        )
        certi_level.save()
        return certi_level
