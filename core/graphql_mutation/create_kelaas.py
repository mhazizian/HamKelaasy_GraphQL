import graphene
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
        if info.context.user.is_authenticated:
            user = info.context.user.person
            if user.type == TEACHER_KEY_WORD:
                Create_kelaas.make_kelaas(user.teacher, data)
                return MessageType(type="success", message="Kelaas added.")

        return MessageType(type="error", message="Permission denied.")

    @staticmethod
    def make_kelaas(teacher, data):
        kelaas = Kelaas(
            title=data.title,
            description=data.description,
        )
        kelaas.save()
        teacher.kelaases.add(kelaas)
        teacher.save()
        for tag_id in data.tags.split(','):
            if Tag.objects.filter(pk=tag_id).exists():
                tag = Tag.objects.get(pk=tag_id)
                kelaas.tags.add(tag)
        kelaas.save()
