import graphene
import core.services as services
from core import HamkelaasyError

from core.graphql_query import KelaasPostType


class Kelaas_post_input(graphene.InputObjectType):
    kelaas_id = graphene.Int(required=True)
    title = graphene.String(default_value="")
    description = graphene.String(default_value="")
    files = graphene.String(description="a string of files id.\n\nexample: '1,2,10,4'")


class Create_kelaas_post(graphene.Mutation):
    class Arguments:
        data = Kelaas_post_input(required=True)

    Output = KelaasPostType

    def mutate(self, info, data):
        return Create_kelaas_post.make_post(info, data)

    @staticmethod
    def make_post(info, data):
        if not info.context.user.is_authenticated:
            raise HamkelaasyError('user not authenticated', status=401)
        user = info.context.user.person

        return services.create_kelaas_post(
            user=user,
            kelaas_id=data.kelaas_id,
            title=data.title,
            description=data.description,
            files=data.files
        )
