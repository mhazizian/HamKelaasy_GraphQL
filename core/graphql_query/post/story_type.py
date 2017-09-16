import graphene
from core.graphql_query.post import PostType


class StoryType(PostType):
    name = "story"

    pic = graphene.String()
    like_count = graphene.Int()

    def resolve_pic(self, info):
        return self.story.pic

    def resolve_like_count(self, info):
        return self.story.like_count


