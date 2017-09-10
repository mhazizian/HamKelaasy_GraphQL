from graphql import GraphQLError

import graphene

from graphql_mutation import Create_kelaas , Create_kelaas_post, Create_story, Upload_file, Assign_badge, Add_comment


class Mutation(graphene.ObjectType):
    create_kelaas = Create_kelaas.Field()
    create_kelaas_post = Create_kelaas_post.Field()
    create_story = Create_story.Field()
    upload_file = Upload_file.Field()
    assign_badge = Assign_badge.Field()
    add_comment = Add_comment.Field()
