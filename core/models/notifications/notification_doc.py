from enum import Enum


class Notification_type(object):
    class Teacher(Enum):
        new_student = 10001
        new_message = 10002
        new_comment = 10003
        new_parent = 10004

    class Parent(Enum):
        new_message = 20001  # also will have conversation id
        new_story = 20002  # also will have kelaas id
        new_comment = 20003  # also will have post id
        child_joined_kelaas = 20004  # also will have child id

    class Student(Enum):
        new_post = 30001  # also will have post id
        new_kelaas_joined = 30002  # also will have kelaas id
        new_badge = 30003  # will also have badge id


notification_doc = {
    Notification_type.Teacher.new_student.value: {
        'related_ids': 'kelaas_id, sutdent_id',
        'related_text': 'student_fistname, student_lastname',
        'description': 'notification for new student joined kelasses',
    },
    Notification_type.Teacher.new_message.value: {
        'related_ids': 'conversation_id, kelaas_id, message_id',
        'related_text': 'message_body',
        'description': 'notification for new message in teachers conversation with parents',
    },
    Notification_type.Teacher.new_comment.value: {
        'related_ids': 'post_id, kelaas_id, writer_id',
        'related_text': 'writer_firstname, writer_lastname, comment_body',
        'description': 'notification for new comment in teachers related kelaases',
    },
    Notification_type.Teacher.new_parent.value: {
        'related_ids': 'kelaas_id, student_id, parent_id',
        'related_text': 'student first name and last name',
        'description': 'notification for new parent joined kelaas',
    },

}
