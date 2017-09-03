import graphene


class StoryType(graphene.ObjectType):
    name = "story"

    id = graphene.Int()
    description = graphene.String()
    shamsi_date = graphene.String()
    pic = graphene.String()
    kelaas = graphene.Field('core.graphql_utilz.KelaasType')

    def resolve_kelaas(story,info):
        return story.kelaas

