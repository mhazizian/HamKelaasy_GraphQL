import graphene
from core.graphql_query.post import PostType
import core.services as services


class StoryType(PostType):
    name = "story"

    pic = graphene.String()
    pics = graphene.List('core.graphql_query.FileType')
    like_count = graphene.Int()
    i_have_liked_it = graphene.Boolean()

    def resolve_pic(self, info):
        return self.story.pic

    def resolve_like_count(self, info):
        user = info.context.user.person
        return services.story__get_likes_count(story=self.story, user=user)

    def resolve_pics(self, info):
        return self.story.pics.all()

    def resolve_i_have_liked_it(self,info):
        user = info.context.user.person

        return self.story.likes.filter(id=user.id).exists()