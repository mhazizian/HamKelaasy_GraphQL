import graphene


from graphene_django.debug import DjangoDebug
import core.schema_query
import core.schema_mutation


class Query(core.schema_query.Query, graphene.ObjectType):
    debug = graphene.Field(DjangoDebug, name='__debug')


class Mutation(core.schema_mutation.Mutation, graphene.ObjectType):
    debug = graphene.Field(DjangoDebug, name='__debug')


schema = graphene.Schema(query=Query, mutation=Mutation)
