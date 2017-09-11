import graphene


class CertificateType(graphene.ObjectType):
    # a Certificate model should be passed
    name = "certificate"

    id = graphene.Int()
    title = graphene.String()
    description = graphene.String()
    pic = graphene.String()
    creator = graphene.Field('core.graphql_query.PersonType')
    shamsi_date = graphene.String()
    time_passed = graphene.String()

    levels = graphene.List('core.graphql_query.CertificateLevelType')

    def resolve_creator(self, info):
        return self.creator

    def resolve_levels(self, info):
        return self.levels.all()


class CertificateLevelType(graphene.ObjectType):
    # a Certificate_level model should be passed
    pic = graphene.String()
    level = graphene.Int()
    level_description = graphene.String()
    shamsi_date = graphene.String()
    time_passed = graphene.String()

    def resolve_pic(self, info):
        return self.pic

    def resolve_level(self, info):
        return self.level

    def resolve_level_description(self, info):
        return self.level_description
