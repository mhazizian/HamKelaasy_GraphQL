import graphene


class KelaasPostType(graphene.ObjectType):
    name = "kelaas post"

    post = graphene.Field('core.graphql_utilz.PostType')
    files = graphene.List('core.graphql_utilz.FileType')

    def resolve_post(kelaasPost, info):
        return kelaasPost.post

    def resolve_files(kelaasPost, info):
        return kelaasPost.files.all()

