import graphene


class PersonCertificateType(graphene.ObjectType):
    # a Certificate model should be passed
    name = "certificate"

    id = graphene.Int()
    title = graphene.String()
    description = graphene.String()
    pic = graphene.String()
    creator = graphene.Field('core.graphql_query.PersonType')

    levels = graphene.List('core.graphql_query.CertificateLinkType')


class CertificateLinkType(graphene.ObjectType):
    # a Certificate_level model should be passed
    pic = graphene.String()
    level = graphene.Int()
    level_description = graphene.String()
    assigner = graphene.Field('core.graphql_query.PersonType')
    time_passed = graphene.String()

    def resolve_pic(self, info):
        return self.certificate_level.pic

    def resolve_level(self, info):
        return self.certificate_level.level

    def resolve_level_description(self, info):
        return self.certificate_level.level_description

    def resolve_assigner(self, info):
        return self.assigner

    def resolve_time_passed(self, info):
        return self.time_passed

