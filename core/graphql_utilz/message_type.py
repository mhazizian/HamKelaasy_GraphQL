import graphene


class MessageType(graphene.ObjectType):
    name = "kelaas"
    type = graphene.String()
    message = graphene.String()
