import graphene
import core.services as services
from core import HamkelaasyError, Error_code

from core.graphql_query import PersonType


class Edit_profile_input(graphene.InputObjectType):
    first_name = graphene.String(default_value="")
    last_name = graphene.String(default_value="")


class Edit_profile(graphene.Mutation):
    class Arguments:
        data = Edit_profile_input(required=True)

    Output = PersonType

    def mutate(self, info, data):
        return Edit_profile.edit(info, data)

    @staticmethod
    def edit(info, data):
        if not info.context.user.is_authenticated:
            raise HamkelaasyError(Error_code.Authentication.User_not_authenticated)
        user = info.context.user.person

        return services.edit_profile(
            user=user,
            new_first_name=data.first_name,
            new_last_name=data.last_name,
        )
