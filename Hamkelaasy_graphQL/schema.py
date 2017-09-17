import graphene

from core.schema_query import Query as core_query
from core.schema_mutation import Mutation as core_mutation


class Query(core_query, graphene.ObjectType):
    class Meta:
        description = "List query support pagination,\n\n" \
                      "in order to user pageination usr two var 'page', 'pageSize'\n\n" \
                      "by default page=1 and if you dont provide any value for them you'll only get first page" \
                      "(for example first 10 item in case pageSize=10)\n\n" \
                      "for example:\n\n" \
                      "(page=2 , pageSize=20)\n\nwill give items from 20 to 40(num 40 not included)\n\n\n\n" \
                      "for more information:\n\n" \
                      "http://graphql.org/learn/queries/\n\n" \
                      "http://graphql.org/learn/serving-over-http/#post-request"


class Mutation(core_mutation, graphene.ObjectType):
    class Meta:
        description = "the result of a Mutation is based on its kind, " \
                      "and in case if failer result will only contain 'error'\n\n\n\n" \
                      "for more information:\n\n" \
                      "http://graphql.org/learn/queries/#mutations\n\n" \
                      "http://graphql.org/learn/serving-over-http/#post-request"


schema = graphene.Schema(query=Query, mutation=Mutation)
