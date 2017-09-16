import graphene
from core.graphql_query.post import PostType


class StoryType(PostType):
    name = "story"

    pic = graphene.String()

    def resolve_pic(self, info):
        return self.story.pic


