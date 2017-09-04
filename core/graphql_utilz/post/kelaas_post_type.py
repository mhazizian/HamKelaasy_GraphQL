import graphene
from core.graphql_utilz.post import PostType


class KelaasPostType(PostType):
    name = "kelaas post"

    files = graphene.List('core.graphql_utilz.FileType')

    def resolve_files(self, info):
        return self.files.all()

