import graphene


class PostType(graphene.ObjectType):
    name = "post"

    id = graphene.Int()
    title = graphene.String()
    description = graphene.String()
    shamsi_date = graphene.String()
    type = graphene.String()

    comments = graphene.List('core.graphql_utilz.CommentType')

    def resolve_comments(self, info):
        return self.comment_set.all()[::-1]

    # kelaas = graphene.Field('core.graphql_utilz.KelaasType')
    #
    # def resolve_kelaas(self, info):
    #     return self.kelaas
