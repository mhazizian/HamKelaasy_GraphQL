import graphene
from core.graphql_utilz import PostType


class StoryType(PostType):
    name = "story"

    pic = graphene.String()


