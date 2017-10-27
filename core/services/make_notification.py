import exceptions as exceptions
import logging

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.utils import timezone

from core import HamkelaasyError
from core.errors_code import Error_code

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from core.models import Parent, TEACHER_KEY_WORD, PARENT_KEY_WORD, Kelaas, KELAAS_POST_KEY_WORD, STORY_KEY_WORD, \
    STUDENT_KEY_WORD, Post, Person, Student, Tag, Comment, Badge_link, Badge, File, Kelaas_post, Story, Conversation, \
    Conversation_message, Certificate, Certificate_link, Certificate_level, Task, System_notification, DIALOG_KEY_WORD, \
    Conversation_dialog, Teacher, Temp_phone_number, Notification

logger = logging.getLogger('core')
usage_logger = logging.getLogger('usage_core')


def join_kelaas_by_parent(student, kelaas):
    Notification.create_teacher__new_student(teacher=kelaas.teacher, student=student, kelaas=kelaas)
    # TODO :create notification for student


def join_kelaas_by_student(student, kelaas):
    Notification.create_teacher__new_student(teacher=kelaas.teacher, student=student, kelaas=kelaas)

    if student.parents:
        pass
        # TODO :create notification for parent


def join_kelaas_by_teacher(student, kelaas):
    pass
    # TODO create notification for student
    # TODO create notification for student's parent


def parent_joined_kelaas(kelaas, student):
    if not student.parents:
        return

    Notification.create_teacher__new_parent(teacher=kelaas.teacher, student=student, kelaas=kelaas)


def parent_setted(student):
    if not student.parents:
        return

    # TODO : send notification for student

    for kelaas in student.kelaases.all():
        parent_joined_kelaas(kelaas=kelaas, student=student)
    pass


def new_comment(comment):
    kelaas = comment.post.kelaas
    Notification.create_teacher__new_comment(teacher=kelaas.teacher, comment=comment, kelaas=kelaas)

    # TODO : create notification for other members?!
