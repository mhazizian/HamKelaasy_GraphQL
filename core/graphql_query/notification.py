import graphene


class NotificationType(graphene.ObjectType):
    name = "notification"

    id = graphene.Int()
    receiver = graphene.Field('core.graphql_query.PersonType')
    has_seen = graphene.Int()

    time_passed = graphene.String()
    shamsi_date = graphene.String()

    type_code = graphene.Int()
    related_id = graphene.Int()
    related_text = graphene.String()
