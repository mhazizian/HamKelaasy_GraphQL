import graphene
from core import HamkelaasyError

from core.graphql_query import MessageType
from core.models import TEACHER_KEY_WORD, File


class File_input(graphene.InputObjectType):
    title = graphene.String()
    description = graphene.String(default_value="")


class Upload_file(graphene.Mutation):
    class Arguments:
        data = File_input(required=True)

    Output = MessageType

    def mutate(self, info, data):
        res = Upload_file.upload(info, data)
        return MessageType(type="success", message=res)

    @staticmethod
    def upload(info, data):
        if not info.context.user.is_authenticated:
            raise HamkelaasyError(4011)
        user = info.context.user.person

        if not user.type == TEACHER_KEY_WORD:
            raise HamkelaasyError('Permission denied', status=403)

        uploaded_file = []
        for f in info.context.FILES.getlist('post-files'):
            temp = File(
                title=data.title,
                description=data.description,
                data=f,
            )
            temp.owner = info.context.user.person
            temp.save()
            uploaded_file.append(temp)

        return ''.join([str(f.id) for f in uploaded_file])
