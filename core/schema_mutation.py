from graphql import GraphQLError

import graphene
from core.models import *

from graphql_mutation import Create_kelaas , Create_kelaas_post, Create_story, File_input


class Mutation(graphene.ObjectType):
    create_kelaas = Create_kelaas.Field()
    create_kelaas_post = Create_kelaas_post.Field()
    create_story = Create_story.Field()
    upload_file = File_input.Field()
