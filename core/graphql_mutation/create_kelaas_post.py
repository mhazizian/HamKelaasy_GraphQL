import graphene
from core.graphql_query import MessageType
from core.models import Kelaas_post, TEACHER_KEY_WORD, File


class Kelaas_post_input(graphene.InputObjectType):
    kelaas_id = graphene.Int()
    title = graphene.String()
    description = graphene.String()
    files = graphene.List(graphene.Int)


class Create_kelaas_post(graphene.Mutation):
    class Arguments:
        data = Kelaas_post_input(required=True)

    Output = MessageType

    def mutate(self, info, data):
        if info.context.user.is_authenticated:
            user = info.context.user.person
            if user.type == TEACHER_KEY_WORD:
                if user.teacher.kelaases.filter(pk=data.kelaas_id).exists():
                    kelaas = user.teacher.kelaases.get(pk=data.kelaas_id)
                    Create_kelaas_post.make_post(kelaas, data, user.teacher)
                    return MessageType(type="success", message="Kelaas added.")

        return MessageType(type="error", message="Permission denied.")

    @staticmethod
    def make_post(kelaas, data, teacher):
        post = Kelaas_post(
            title=data.title,
            description=data.description,
            kelaas=kelaas,
            owner=teacher,
        )
        post.save()
        for file_id in data.files:
            if File.objects.filter(pk=file_id).exists():
                input_file = File.objects.get(pk=file_id)
                post.files.add(input_file)
        post.save()
