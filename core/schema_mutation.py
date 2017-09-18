import graphene

from graphql_mutation import Create_kelaas, Create_kelaas_post, Create_story, Upload_file, Assign_badge, Add_comment, \
    Join_kelaas, Add_child, Send_message, Create_convesation, Assign_certificate, Create_certificate, \
    Create_certificate_level, Perform_task


class Mutation(graphene.ObjectType):
    create_kelaas = Create_kelaas.Field()
    join_kelaas = Join_kelaas.Field()

    upload_file = Upload_file.Field()
    create_kelaas_post = Create_kelaas_post.Field()
    create_story = Create_story.Field()
    add_comment = Add_comment.Field()

    create_conversation = Create_convesation.Field()
    send_message = Send_message.Field()

    add_child = Add_child.Field()
    assign_badge = Assign_badge.Field()
    assign_certificate = Assign_certificate.Field()
    create_certificate = Create_certificate.Field()
    create_certificate_level = Create_certificate_level.Field()

    perform_task = Perform_task.Field()
