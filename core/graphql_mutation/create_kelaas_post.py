import graphene
from core import myGraphQLError

from core.graphql_query import KelaasPostType
from core.models import Kelaas_post, TEACHER_KEY_WORD, File, Kelaas


class Kelaas_post_input(graphene.InputObjectType):
    kelaas_id = graphene.Int(required=True)
    title = graphene.String(default_value="")
    description = graphene.String(default_value="")
    files = graphene.String(description="a string of files id.\n\nexample: '1,2,10,4'")


class Create_kelaas_post(graphene.Mutation):
    class Arguments:
        data = Kelaas_post_input(required=True)

    Output = KelaasPostType

    def mutate(self, info, data):
        return Create_kelaas_post.make_post(info, data)

    @staticmethod
    def make_post(info, data):
        if not info.context.user.is_authenticated:
            raise myGraphQLError('user not authenticated', status=401)
        user = info.context.user.person

        if not user.type == TEACHER_KEY_WORD:
            raise myGraphQLError('Permission denied', status=403)

        try:
            kelaas = user.teacher.kelaases.get(pk=data.kelaas_id)
        except Kelaas.DoesNotExist:
            raise myGraphQLError('Kelaas not found', status=404)

        post = Kelaas_post(
            title=data.title,
            description=data.description,
            kelaas=kelaas,
            owner=user.teacher,
        )
        post.save()
        for file_id in data.files.split(','):
            if File.objects.filter(pk=file_id).exists():
                input_file = File.objects.get(pk=file_id)
                post.files.add(input_file)
        post.save()

        return post
