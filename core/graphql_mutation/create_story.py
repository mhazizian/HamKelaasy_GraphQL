import graphene
from core import myGraphQLError

from core.graphql_query import MessageType
from core.models import Story, TEACHER_KEY_WORD, File


class Story_input(graphene.InputObjectType):
    kelaas_id = graphene.Int(required=True)
    title = graphene.String(default_value="")
    description = graphene.String(default_value="")
    pic = graphene.Int(description="uploaded pic id")


class Create_story(graphene.Mutation):
    class Arguments:
        data = Story_input(required=True)

    Output = MessageType

    def mutate(self, info, data):
        if info.context.user.is_authenticated:
            user = info.context.user.person
            if user.type == TEACHER_KEY_WORD:
                if user.teacher.kelaases.filter(pk=data.kelaas_id).exists():
                    kelaas = user.teacher.kelaases.get(pk=data.kelaas_id)
                    Create_story.make_story(info, kelaas, data, user.teacher)
                    return MessageType(type="success", message="Story added.")
                raise myGraphQLError('Bad data input')

        raise myGraphQLError('Permission denied')

    @staticmethod
    def make_story(info, kelaas, data, teacher):
        story = Story(
            title=data.title,
            description=data.description,
            kelaas=kelaas,
            owner=teacher,
        )
        story.save()

        if data.pic:
            if File.objects.filter(pk=data.pic).exists():
                story.story_pic_id = data.pic
        story.save()
        return True