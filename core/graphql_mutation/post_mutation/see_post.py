import graphene
import core.services as services
from core import HamkelaasyError
from core import Error_code

from core.graphql_query import PostType


class See_post_input(graphene.InputObjectType):
    post_ids = graphene.String(required=True, description="posts ids seperated by , example:'123,131,431'")


class See_post(graphene.Mutation):
    class Arguments:
        data = See_post_input(required=True)

    Output = graphene.List(PostType)

    def mutate(self, info, data):
        return See_post.make_seen(info, data)

    @staticmethod
    def make_seen(info, data):
        if not info.context.user.is_authenticated:
            raise HamkelaasyError(Error_code.Authentication.User_not_authenticated)
        user = info.context.user.person

        return services.see_post(user=user, post_ids=data.post_ids)
