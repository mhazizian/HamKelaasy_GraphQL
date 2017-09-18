import graphene
from core import myGraphQLError

from core.graphql_query import TaskType
from core.models import Task


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
            raise myGraphQLError('user not authenticated', status=401)
        user = info.context.user.person

        try:
            task = Task.objects.get(pk=data.task_id)
            if not task.student_id == user.id:
                raise myGraphQLError('Permission denied', status=403)

            task.is_done = Task
            task.save()
            return task

        except Task.DoesNotExist:
            raise myGraphQLError('Task not found', status=404)
