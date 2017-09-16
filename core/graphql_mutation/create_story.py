import graphene
from core import myGraphQLError

from core.graphql_query import StoryType
from core.models import Story, TEACHER_KEY_WORD, File, Kelaas


class Story_input(graphene.InputObjectType):
    kelaas_id = graphene.Int(required=True)
    title = graphene.String(default_value="")
    description = graphene.String(default_value="")
    pic = graphene.Int(description="uploaded pic id")


class Create_story(graphene.Mutation):
    class Arguments:
        data = Story_input(required=True)

    Output = StoryType

    def mutate(self, info, data):
        return Create_story.make_story(info, data)

    @staticmethod
    def make_story(info, data):
        if not info.context.user.is_authenticated:
            raise myGraphQLError('user not authenticated', status=401)
        user = info.context.user.person

        if not user.type == TEACHER_KEY_WORD:
            raise myGraphQLError('Permission denied', status=403)

        try:
            kelaas = user.teacher.kelaases.get(pk=data.kelaas_id)
        except Kelaas.DoesNotExist:
            raise myGraphQLError('Kelaas not found', status=404)

        story = Story(
            title=data.title,
            description=data.description,
            kelaas=kelaas,
            owner=user.teacher,
        )
        story.save()

        if data.pic:
            if File.objects.filter(pk=data.pic).exists():
                story.story_pic_id = data.pic
        story.save()
        return story
