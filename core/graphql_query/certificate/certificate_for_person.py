import graphene


class PersonCertificateType(graphene.ObjectType):
    # a Certificate model should be passed
    name = "certificate"

    id = graphene.Int()
    title = graphene.String()
    description = graphene.String()
    pic = graphene.String()
    creator = graphene.Field('core.graphql_query.PersonType')
    shamsi_date = graphene.String()
    time_passed = graphene.String()

    levels = graphene.List('core.graphql_query.CertificateLinkType')

