import graphene


class StoryType(graphene.ObjectType):
    name = "story"

    post = graphene.Field('core.graphql_utilz.PostType')
    pic = graphene.String()

    def resolve_post(story, info):
        return story.post

