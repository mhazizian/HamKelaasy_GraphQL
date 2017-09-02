import graphene


class TagType(graphene.ObjectType):
    name = "tag"
    description = "..."

    id = graphene.Int()
    title = graphene.String()