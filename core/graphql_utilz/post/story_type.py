import graphene
from core.graphql_utilz.post import PostType


class StoryType(PostType):
    name = "story"

    pic = graphene.String()


