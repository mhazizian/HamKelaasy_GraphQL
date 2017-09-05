import graphene


class CertificateType(graphene.ObjectType):
    # a Certificate model should be passed
    name = "certificate"

    id = graphene.Int()
    title = graphene.String()
    description = graphene.String()
    certificate_pic = graphene.String()
    creator = graphene.Field('core.graphql_query.PersonType')

    pic = graphene.String()
    level = graphene.Int()
    level_description = graphene.String()

    def resolve_title(self, info):
        return self.type.title

    def resolve_description (self, info):
        return self.type.description

    def resolve_certificate_pic(self, info):
        return self.type.pic

    def resolve_creator(self, info):
        return self.type.creator

    def resolve_pic(self, info):
        return self.pic

    def resolve_level(self, info):
        return self.level

    def resolve_level_description(self, info):
        return self.level_description