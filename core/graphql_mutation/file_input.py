import graphene
from core.models import File


class FileInput(graphene.InputObjectType):
    url = graphene.String(required=True)
    title = graphene.String()


def make_file(data, owner):
    file = File(
        title=data.title,
        url=data.url,
        owner=owner,
    )
    file.save()
    return file
