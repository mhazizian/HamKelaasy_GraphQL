import graphene
from core.graphql_query.post import PostType
import core.services as services


class StoryType(PostType):
    name = "story"

    pic = graphene.String()
    like_count = graphene.Int()

    def resolve_pic(self, info):
        return self.story.pic

    def resolve_like_count(self, info):
        user = info.context.user.person
        return services.story__get_likes_count(story=self.story, user=user)
