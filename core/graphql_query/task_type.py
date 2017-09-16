import graphene


class TaskType(graphene.ObjectType):
    name = "task"

    body = graphene.String()
    is_done = graphene.Boolean()

    kelaas = graphene.Field('core.graphql_query.KelaasType')
    student = graphene.Field('core.graphql_query.StudentType')

    time_passed = graphene.String()
    shamsi_date = graphene.String()
    remaning_time = graphene.String()
