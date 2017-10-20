import graphene
import core.services as services
from core import HamkelaasyError
from core import Error_code

from core.graphql_query import NotificationType


class Seen_notification_input(graphene.InputObjectType):
    notification_id = graphene.String(required=True)


class Make_notification_seen(graphene.Mutation):
    class Arguments:
        data = Seen_notification_input(required=True)

    Output = NotificationType

    def mutate(self, info, data):
        return Make_notification_seen.make_seen(info, data)

    @staticmethod
    def make_seen(info, data):
        if not info.context.user.is_authenticated:
            raise HamkelaasyError(Error_code.Authentication.User_not_authenticated)
        user = info.context.user.person

        return services.make_notification_seen(user=user, notification_id=data.notification_id)
