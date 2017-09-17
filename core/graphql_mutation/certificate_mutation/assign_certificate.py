import graphene
from core import myGraphQLError

from core.graphql_query import CertificateLinkType
from core.models import Certificate, Person, Certificate_link


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

        try:
            certificate_level = Certificate.objects.get(pk=data.type_id).levels.filter(level=data.level).first()
            owner = Person.objects.get(pk=data.owner_id)

            # TODO Permission checking ?!
            # TODO continuously levels checking
            # TODO same certificate level from different persons!!!

            if owner.certificates.filter(certificate_level=certificate_level, assigner_id=user.id).exists():
                return owner.certificates.filter(certificate_level=certificate_level, assigner_id=user.id).first()

            certificate_link = Certificate_link(
                certificate_level=certificate_level,
                owner=owner,
                assigner=user
            )
            certificate_link.save()
            return certificate_link

        except Certificate.DoesNotExist:
            raise myGraphQLError('Certificate not found', status=404)
        except Person.DoesNotExist:
            raise myGraphQLError('Owner not found', status=404)
