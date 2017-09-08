import graphene


class BadgeModelType(graphene.ObjectType):
    # a Badge_type model should be passed
    title = graphene.String()
    pic = graphene.String()

    def resolve_pic(self, info):
        return self.pic.url


class BadgeLink(graphene.ObjectType):
    # a Badge_link model should be passed
    name = "badge"

    title = graphene.String()
    pic = graphene.String()
    count = graphene.Int
    kelaas = graphene.Field('core.graphql_query.KelaasType')