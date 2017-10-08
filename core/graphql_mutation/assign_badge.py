import graphene
import core.services as services
from core import HamkelaasyError
from core import Error_code
from core.graphql_query import BadgeLink


class Assign_badge_input(graphene.InputObjectType):
    kelaas_id = graphene.Int(required=True)
    badges = graphene.String(required=True, description="a string of badge_id.\n\nexample: '1,2,10,4'")
    student_id = graphene.Int(required=True)


class Assign_badge(graphene.Mutation):
    class Arguments:
        data = Assign_badge_input(required=True)

    Output = BadgeLink

    def mutate(self, info, data):
        return Assign_badge.assign_badge(info, data)

    @staticmethod
    def assign_badge(info, data):
        if not info.context.user.is_authenticated:
            raise HamkelaasyError(Error_code.Authentication.User_not_authenticated)
        user = info.context.user.person

        return services.assign_badge(
            user=user,
            kelaas_id=data.kelaas_id,
            student_id=data.student_id,
            badges=data.badges,
        )
