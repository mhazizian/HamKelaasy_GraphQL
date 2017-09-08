import graphene

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
        if info.context.user.is_authenticated:
            user = info.context.user.person
            if user.type == TEACHER_KEY_WORD:
                res = Upload_file.upload(info, data)
                return MessageType(type="success", message=res)

        return MessageType(type="error", message="Permission denied.")

    @staticmethod
    def upload(info, data):
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

        # return [f.id for f in uploaded_file]
        return ''.join([str(f.id) for f in uploaded_file])