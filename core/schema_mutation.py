import graphene

from graphql_mutation import Create_kelaas, Create_kelaas_post, Create_story, Assign_badge, Add_comment, \
    Join_kelaas, Add_child, Send_message, Assign_certificate, Create_certificate, \
    Create_certificate_level, Perform_task, Add_child_by_token, Delete_comment, Delete_post, Join_kelaas_for_parent, \
    Create_parent_child, Create_student_for_kelaas, Remove_student_from_kelaas, Make_notification_seen, Edit_profile, \
    Like_story, Dislike_story, See_post


class Mutation(graphene.ObjectType):
    create_kelaas = Create_kelaas.Field()
    join_kelaas = Join_kelaas.Field()
    join_kelaas_for_parent = Join_kelaas_for_parent.Field()
    remove_student_from_kelaas = Remove_student_from_kelaas.Field()

    # upload_file = Upload_file.Field()
    create_kelaas_post = Create_kelaas_post.Field()
    create_story = Create_story.Field()
    delete_post = Delete_post.Field()

    add_comment = Add_comment.Field()
    delete_comment = Delete_comment.Field()

    # create_conversation = Create_convesation.Field()
    send_message = Send_message.Field()

    add_child = Add_child.Field()
    add_child_by_token = Add_child_by_token.Field()
    create_parent_child = Create_parent_child.Field()

    assign_badge = Assign_badge.Field()
    assign_certificate = Assign_certificate.Field()
    create_certificate = Create_certificate.Field()
    create_certificate_level = Create_certificate_level.Field()

    perform_task = Perform_task.Field()

    create_student_for_kelaas = Create_student_for_kelaas.Field()
    make_notification_seen = Make_notification_seen.Field()
    edit_profile = Edit_profile.Field()

    like_story = Like_story.Field()
    dislike_story = Dislike_story.Field()
    see_post = See_post.Field()