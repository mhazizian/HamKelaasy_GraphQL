import graphene
from core import myGraphQLError

from core.graphql_query import MessageType
from core.models import Tag, Kelaas, TEACHER_KEY_WORD


class Kelaas_input(graphene.InputObjectType):
    title = graphene.String(required=True)
    description = graphene.String(default_value="")
    tags = graphene.String(description="a string of tag's id,\n\n example: '1,10,4,3,'")


class Create_kelaas(graphene.Mutation):
    class Arguments:
        data = Kelaas_input(required=True)

    Output = MessageType

    def mutate(self, info, data):
        if Create_kelaas.make_kelaas(info, data):
            return MessageType(type="success", message="Kelaas added.")

    @staticmethod
    def make_kelaas(info, data):
        if not info.context.user.is_authenticated:
            raise myGraphQLError('user not authenticated', status=401)
        user = info.context.user.person

        if not user.type == TEACHER_KEY_WORD:
            raise myGraphQLError('Permission denied', status=403)

        kelaas = Kelaas(
            title=data.title,
            description=data.description,
        )
        kelaas.save()
        user.teacher.kelaases.add(kelaas)
        user.teacher.save()
        for tag_id in data.tags.split(','):
            if Tag.objects.filter(pk=tag_id).exists():
                tag = Tag.objects.get(pk=tag_id)
                kelaas.tags.add(tag)
        kelaas.save()
