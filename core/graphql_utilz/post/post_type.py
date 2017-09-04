import graphene


class PostType(graphene.ObjectType):
    name = "post"

    id = graphene.Int()
    title = graphene.String()
    description = graphene.String()
    shamsi_date = graphene.String()
    type = graphene.String()

    # kelaas = graphene.Field('core.graphql_utilz.KelaasType')
    #
    # def resolve_kelaas(self, info):
    #     return self.kelaas
