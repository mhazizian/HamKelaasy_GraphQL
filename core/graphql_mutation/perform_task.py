import graphene
import core.services as services
from core import HamkelaasyError

from core.graphql_query import TaskType


class perform_task_input(graphene.InputObjectType):
    task_id = graphene.Int(required=True)


class Perform_task(graphene.Mutation):
    class Arguments:
        data = perform_task_input(required=True)

    Output = TaskType

    def mutate(self, info, data):
        return Perform_task.perform(info, data)

    @staticmethod
    def perform(info, data):
        if not info.context.user.is_authenticated:
            raise HamkelaasyError('user not authenticated', status=401)
        user = info.context.user.person

        return services.perform_task(
            user=user,
            task_id=data.task_id
        )
