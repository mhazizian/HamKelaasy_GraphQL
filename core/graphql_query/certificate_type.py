import graphene


class CertificateType(graphene.ObjectType):
    # a certificate_link model should be passed
    name = "certificate"

    title = graphene.String()
    pic = graphene.String()
    count = graphene.Int
    kelaas = graphene.Field('core.graphql_query.KelaasType')

    def resolve_kelaas(self, info):
        return self.badge.kelaas
