from enum import Enum


class Notification_type(object):
    class Teacher(Enum):
        new_student = 10001
        new_message = 10002  # also will have conversation id
        new_comment = 10003  # also will have post id
        student_added_parent = 10004  # also will have student id

    class Parent(Enum):
        new_message = 20001  # also will have conversation id
        new_story = 20002  # also will have kelaas id
        new_comment = 20003  # also will have post id
        child_joined_kelaas = 20004  # also will have child id

    class Student(Enum):
        new_post = 30001  # also will have post id
        new_kelaas_joined = 30002  # also will have kelaas id
        new_badge = 30003  # will also have badge id
