import graphene


class KelaasPostType(graphene.ObjectType):
    name = "kelaas post"

    post = graphene.Field('core.graphql_utilz.PostType')
    files = graphene.List('core.graphql_utilz.FileType')

    def resolve_post(self, info):
        return self.post

    def resolve_files(self, info):
        return self.files.all()

