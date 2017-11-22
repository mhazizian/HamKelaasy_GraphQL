import graphene
import core.services as services
from core import HamkelaasyError
from core import Error_code

from core.graphql_query import KelaasPostType


class Edit_kelaas_post_input(graphene.InputObjectType):
    story_id = graphene.Int(required=True)
    description = graphene.String(required=True)
    title = graphene.String(required=True)


class Edit_kelaas_post(graphene.Mutation):
    class Arguments:
        data = Edit_kelaas_post_input(required=True)

    Output = KelaasPostType

    def mutate(self, info, data):
        return Edit_kelaas_post.edit(info, data)

    @staticmethod
    def edit(info, data):
        if not info.context.user.is_authenticated:
            raise HamkelaasyError(Error_code.Authentication.User_not_authenticated)
        user = info.context.user.person

        return services.edit_kelaas_post(
            user=user,
            kelaas_post_id=data.story_id,
            title=data.title,
            description=data.description,
        )
