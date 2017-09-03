import graphene


class FileType(graphene.ObjectType):
    name = "file"

    title = graphene.String()
    description = graphene.String()
    url = graphene.String()

    def resolve_url(file, info):
        return file.data.url
