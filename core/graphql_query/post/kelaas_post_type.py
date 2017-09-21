import graphene
from core.graphql_query.post import PostType
import core.services as services


class KelaasPostType(PostType):
    name = "kelaas post"

    files = graphene.List('core.graphql_query.FileType')

    def resolve_files(self, info):
        user = info.context.user.person
        return services.kelaas_post__get_files(kelaas_post=self.kelaas_post, user=user)
