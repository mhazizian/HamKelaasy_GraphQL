from graphql import GraphQLError

import graphene
from core.models import *

from graphql_mutation import Create_kelaas





class Mutation(graphene.ObjectType):
    create_kelaas = Create_kelaas.Field()
