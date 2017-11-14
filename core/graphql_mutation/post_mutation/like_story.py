import graphene
import core.services as services
from core import HamkelaasyError
from core import Error_code

from core.graphql_query import StoryType


class Like_story_input(graphene.InputObjectType):
    story_id = graphene.Int(required=True)


class Like_story(graphene.Mutation):
    class Arguments:
        data = Like_story_input(required=True)

    Output = StoryType

    def mutate(self, info, data):
        return Like_story.like(info, data)

    @staticmethod
    def like(info, data):
        if not info.context.user.is_authenticated:
            raise HamkelaasyError(Error_code.Authentication.User_not_authenticated)
        user = info.context.user.person

        return services.like_story(user=user, story_id=data.story_id)
