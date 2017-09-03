import graphene


class TagType(graphene.ObjectType):
    name = "tag"

    id = graphene.Int()
    title = graphene.String()