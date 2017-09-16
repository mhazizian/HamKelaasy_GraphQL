import graphene

from graphql_mutation import Create_kelaas, Create_kelaas_post, Create_story, Upload_file, Assign_badge, Add_comment, \
    Join_kelaas, Add_child, Send_message, Create_convesation


class Mutation(graphene.ObjectType):
    create_kelaas = Create_kelaas.Field()
    create_kelaas_post = Create_kelaas_post.Field()
    create_story = Create_story.Field()
    upload_file = Upload_file.Field()
    assign_badge = Assign_badge.Field()
    add_comment = Add_comment.Field()
    join_kelaas = Join_kelaas.Field()
    add_child = Add_child.Field()
    send_message = Send_message.Field()
    create_conversation = Create_convesation.Field()
