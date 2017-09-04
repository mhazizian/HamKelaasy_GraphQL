import graphene


class BadgeType(graphene.ObjectType):
    # a Badge_link model should be passed
    name = "badge"

    title = graphene.String()
    pic = graphene.String()
    count = graphene.Int
    kelaas = graphene.Field('core.graphql_utilz.KelaasType')

    def resolve_kelaas(self, info):
        return self.badge.kelaas

    def resolve_title(self, info):
        return self.badge.type.title
