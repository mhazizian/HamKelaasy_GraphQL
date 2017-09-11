import graphene
from core.graphql_query.post import PostType


class KelaasPostType(PostType):
    name = "kelaas post"

    files = graphene.List('core.graphql_query.FileType')

    def resolve_files(self, info):
        return self.kelaas_post.files.all()[:]

