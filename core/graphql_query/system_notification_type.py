import graphene


class SystemNotificationType(graphene.ObjectType):
    name = "system notification"

    title = graphene.String()
    description = graphene.String()
    type = graphene.String()
    time_passed = graphene.String()
    shamsi_date = graphene.String()