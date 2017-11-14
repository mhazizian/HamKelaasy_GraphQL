import graphene
import core.services as services
from core import HamkelaasyError
from core import Error_code

from core.graphql_query import StoryType


class Dislike_story_input(graphene.InputObjectType):
    story_id = graphene.Int(required=True)


class Dislike_story(graphene.Mutation):
    class Arguments:
        data = Dislike_story_input(required=True)

    Output = StoryType

    def mutate(self, info, data):
        return Dislike_story.dislike(info, data)

    @staticmethod
    def dislike(info, data):
        if not info.context.user.is_authenticated:
            raise HamkelaasyError(Error_code.Authentication.User_not_authenticated)
        user = info.context.user.person

        return services.dislike_story(user=user, story_id=data.story_id)
