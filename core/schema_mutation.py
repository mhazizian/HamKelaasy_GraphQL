from graphql import GraphQLError

import graphene
from core.models import *

from graphql_utilz import MessageType


class Kelaas_input(graphene.InputObjectType):
    title = graphene.String()
    description = graphene.String()
    tags = graphene.String()


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
        teacher.kelasses.add(kelaas)
        teacher.save()
        for tag_id in data.tags.split(','):
            if Tag.objects.filter(pk=tag_id).exists():
                tag = Tag.objects.get(pk=tag_id)
                kelaas.tags.add(tag)
        kelaas.save()


class Mutation(graphene.ObjectType):
    create_kelaas = Create_kelaas.Field()
