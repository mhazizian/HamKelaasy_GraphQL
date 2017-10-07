import exceptions as exceptions
import json

import requests
from datetime import timedelta
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import IntegrityError
from django.utils import timezone
from rest_framework.authtoken.models import Token
import logging

from django.contrib.auth.models import User
from core import HamkelaasyError
from core.models import Parent, TEACHER_KEY_WORD, PARENT_KEY_WORD, Kelaas, KELAAS_POST_KEY_WORD, STORY_KEY_WORD, \
    STUDENT_KEY_WORD, Post, Person, Student, Tag, Comment, Badge_link, Badge, File, Kelaas_post, Story, Conversation, \
    Conversation_message, Certificate, Certificate_link, Certificate_level, Task, System_notification, DIALOG_KEY_WORD, \
    Conversation_dialog, Teacher, Temp_phone_number

logger = logging.getLogger('core')
DEFAULT_PAGE_SIZE = 10
MAX_PAGE_SIZE = 100


def represents_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def represent_phone_number(s):
    if not represents_int(s):
        raise HamkelaasyError(4001)

    if len(s) == 11 and s[0] == '0':
        s = '98' + s[1:]
    if len(s) == 10 and s[0] == '9':
        s = '98' + s[:]
    if len(s) != 12 or (not s[:2] == '98'):
        raise HamkelaasyError(4001)

    return s


def apply_pagination(input_list, page=1, page_size=DEFAULT_PAGE_SIZE):
    page_size = min(MAX_PAGE_SIZE, page_size)
    paginator = Paginator(input_list, page_size)

    try:
        res = paginator.page(page)
    except PageNotAnInteger:
        res = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver nothing.
        res = []

    return res


def create_parent(phone, first_name, last_name, password):
    user = User(username=phone)
    user.save()

    parent = Parent(
        user=user,
        first_name=first_name,
        last_name=last_name,
        password=password,
        phone_number=phone,
        phone_number_verified=True,
    )
    parent.save()
    return parent


def create_teacher(phone, first_name, last_name, password, gender):
    user = User(username=phone)
    user.save()

    teacher = Teacher(
        user=user,
        first_name=first_name,
        last_name=last_name,
        password=password,
        phone_number=phone,
        phone_number_verified=True,
        gender=gender,
    )
    teacher.save()
    return teacher


def create_incomplete_student(first_name, last_name, gender, age):
    student = Student(
        user=None,
        first_name=first_name,
        last_name=last_name,
        gender=gender,
        age=age,
    )
    student.save()
    return student


def create_parent_child(user, first_name, last_name, gender, age):
    if user.type != PARENT_KEY_WORD:
        raise HamkelaasyError(4031)

    student = create_incomplete_student(first_name, last_name, gender, age)

    student.parents = user.parent
    student.save()
    return student


def create_student_for_kelaas(user, first_name, last_name, gender, age, kelaas_id):
    if user.type != TEACHER_KEY_WORD:
        raise HamkelaasyError(4031)
    try:
        kelaas = Kelaas.objects.get(id=kelaas_id)
        student = create_incomplete_student(first_name, last_name, gender, age)

        if kelaas.gender != 2 and kelaas.gender != student.gender:
            raise HamkelaasyError(4007)

        kelaas.students.add(student)
        kelaas.save()
        return student
    except Kelaas.DoesNotExist:
        raise HamkelaasyError(4041)


def parent_has_access_to_kelaas(kelaas, parent):
    for student in parent.childes.all():
        if kelaas.students.filter(pk=student.id).exists():
            return True
    return False


def teacher_has_access_to_kelaas(kelaas, teacher):
    if kelaas.teacher.id == teacher.id:
        return True
    return False


def send_sms(phone_number, code):
    r = requests.post(
        "http://sms.3300.ir/services/wsSend.ashx",
        {
            'username': 'nbwa12826',
            'password': '260916',
            'mobile': phone_number,
            'message': unicode(code),
            'type': 2
        }
    )
    res = json.loads(r.text)
    if res['status'] < 0:
        return True
    if res['status'] == 103 or res['status'] == 1 or res['status'] == 2:
        raise HamkelaasyError(4001)
    if res['status'] == 15:
        raise HamkelaasyError(5031)

    raise HamkelaasyError(5032)


def init_phone_number(phone_number, is_for_registration=True):
    phone_number = represent_phone_number(phone_number)

    if Temp_phone_number.objects.filter(pk=phone_number).exists():
        phone = Temp_phone_number.objects.get(pk=phone_number)

        if is_for_registration and phone.is_registered:
            raise HamkelaasyError(4002)
        if (not is_for_registration) and (not phone.is_registered):
            raise HamkelaasyError(4003)

        # TODO change 10 sec to 60 sec in production.
        if timezone.now() - phone.last_send_sms_time < timedelta(seconds=10):
            raise HamkelaasyError(4004)

        phone.re_init()
    else:
        if not is_for_registration:
            raise HamkelaasyError(4003)

        phone = Temp_phone_number(phone_number=phone_number)
        phone.save()

    if not send_sms(phone_number=phone.phone_number, code=phone.code):
        phone.delete()
        raise HamkelaasyError(4001)


def validate_phone_number(phone_number, code):
    phone_number = represent_phone_number(phone_number)

    try:
        phone = Temp_phone_number.objects.get(pk=phone_number)

        if code == phone.code:
            phone.is_validated = True
            phone.save()
            return phone.validator

        return False
    except Temp_phone_number.DoesNotExist:
        raise HamkelaasyError(4003)


def reset_password_by_phone_number(phone_number, validator, new_password):
    phone = represent_phone_number(phone_number)

    try:
        temp_phone = Temp_phone_number.objects.get(pk=phone)
        if not temp_phone.is_registered:
            raise HamkelaasyError(4003)

        if (not temp_phone.is_validated) or (not temp_phone.validator == validator):
            raise HamkelaasyError(4005)

        user = User.objects.get(username=temp_phone.phone)
        user.person.password = new_password
        # TODO apply hashing
        user.person.save()

    except Temp_phone_number.DoesNotExist:
        raise HamkelaasyError(4003)
    except User.DoesNotExist:
        # TODO raise exception
        pass


def create_user_PT(phone, validator, first_name, last_name, password, type, gender=1):
    phone = represent_phone_number(phone)

    try:
        temp_phone = Temp_phone_number.objects.get(pk=phone)
        if temp_phone.is_registered:
            raise HamkelaasyError(4002)

        if (not temp_phone.is_validated) or (not temp_phone.validator == validator):
            raise HamkelaasyError(4005)

        temp_phone.is_registered = True
        temp_phone.save()

        if type == TEACHER_KEY_WORD:
            return create_teacher(
                phone=phone,
                first_name=first_name,
                last_name=last_name,
                password=password,
                gender=gender
            )

        if type == PARENT_KEY_WORD:
            return create_parent(
                phone=phone,
                first_name=first_name,
                last_name=last_name,
                password=password,
            )

    except Temp_phone_number.DoesNotExist:
        raise HamkelaasyError(4003)
    except IntegrityError:
        # TODO do something
        pass


# ______________________________________________________________________________________________________
# ______________________________________________________________________________________________________

def get_kelaas_by_invite_code(invite_code):
    try:
        return Kelaas.objects.get(invite_code=invite_code)
    except Kelaas.DoesNotExist:
        raise HamkelaasyError(4041)


def get_student(user, **kwargs):
    if user.type == STUDENT_KEY_WORD:
        return user.student

    if not 'id' in kwargs:
        raise HamkelaasyError(4006)
    id = kwargs['id']

    if user.type == PARENT_KEY_WORD:
        try:
            return user.parent.childes.get(pk=id)
        except Student.DoesNotExist:
            raise HamkelaasyError(4042)

    if user.type == TEACHER_KEY_WORD:
        for teacher_kelaas in user.teacher.kelaases.all():
            if teacher_kelaas.students.filter(pk=id).exists():
                return teacher_kelaas.students.get(pk=id)
        raise HamkelaasyError(4042)


def get_students(user, **kwargs):
    if user.type == PARENT_KEY_WORD:
        return user.parent.childes.all()

    if user.type == TEACHER_KEY_WORD:
        if 'kelaas_id' in kwargs:
            try:
                return Kelaas.objects.get(pk=kwargs['kelaas_id']).students.all()
            except Kelaas.DoesNotExist:
                raise HamkelaasyError(4041)

    raise HamkelaasyError(4032)


def get_kelaas(user, kelaas_id):
    if user.type == TEACHER_KEY_WORD:
        try:
            return user.teacher.kelaases.get(pk=kelaas_id)
        except Kelaas.DoesNotExist:
            raise HamkelaasyError(4041)

    if user.type == PARENT_KEY_WORD:
        for student in user.parent.childes.all():
            if student.kelaases.filter(pk=kelaas_id).exists():
                return student.kelaases.get(pk=kelaas_id)
        raise HamkelaasyError(4041)

    if user.type == STUDENT_KEY_WORD:
        try:
            return user.student.kelaases.get(pk=kelaas_id)
        except Kelaas.DoesNotExist:
            raise HamkelaasyError(4041)


def get_kelaases(user, **kwargs):
    if user.type == TEACHER_KEY_WORD:
        return user.teacher.kelaases.all()

    if user.type == PARENT_KEY_WORD:
        try:
            return user.parent.childes.get(pk=kwargs['student_id']).kelaases.all()
        except exceptions.KeyError:
            raise HamkelaasyError(4006)
        except Student.DoesNotExist:
            raise HamkelaasyError(4042)

    if user.type == STUDENT_KEY_WORD:
        return user.student.kelaases.all()


def get_teacher(user):
    if user.type == TEACHER_KEY_WORD:
        return user.teacher

    raise HamkelaasyError(4032)


def get_parent(user, **kwargs):
    if user.type == PARENT_KEY_WORD:
        return user.parent

    if user.type == TEACHER_KEY_WORD:
        try:
            # TODO check later
            parent = Parent.objects.get(pk=kwargs['id'])
            for student in parent.childes.all():
                if user.teacher.kelaases.filter(students__in=[student.id]).exists():
                    return parent

        except Parent.DoesNotExist:
            raise HamkelaasyError(4043)
        except exceptions.KeyError:
            raise HamkelaasyError(4006)

    raise HamkelaasyError(4032)


def get_badge_types(**kwargs):
    if 'id' in kwargs:
        id = kwargs['id']
        return Badge.objects.get(pk=id)

    return Badge.objects.all()


def get_certificate(id):
    try:
        return Certificate.objects.get(pk=id)
    except Certificate.DoesNotExist:
        raise HamkelaasyError(4044)


def get_tags():
    return Tag.objects.all()


def get_conversation(user, conversation_id):
    try:
        conversation = Conversation.objects.get(pk=conversation_id)
        if conversation.members.filter(id=user.id).exists():
            return conversation
    except Conversation.DoesNotExist:
        raise HamkelaasyError(4045)

    raise HamkelaasyError(4032)


def get_system_notifications(user, new=False):
    if new and not user.last_sys_notification_seen:
        response = System_notification.objects.filter(create_date__gte=user.last_sys_notofication_seen)
        user.last_sys_notification_seen = timezone.now()
        user.save()
        return response

    user.last_sys_notification_seen = timezone.now()
    user.save()
    return System_notification.objects.all()


# ______________________________________________________________________________________________________
# ______________________________________________________________________________________________________


def parent__get_childes(parent, user, **kwargs):
    if parent.id == user.id:
        return parent.childes.all()

    if user.type == TEACHER_KEY_WORD:
        if 'kelaas_id' in kwargs:
            if user.teacher.kelaases.filter(kelaas_id=kwargs['kelaas_id']).exist():
                return parent.childes.filter(kelaases__in=[kwargs['kelaas_id']])
            raise HamkelaasyError(4032)

        result = []
        # user.kelaases.filter(students__in=[child.id for child in parent.childes.all()])
        for child in parent.childes.all():
            if child.kelaases.filter(teacher_id=user.id).exists():
                result.append(child)
        return result

    raise HamkelaasyError(4032)


def parent__get_child(parent, user, childe_id):
    try:
        if parent.id == user.id:
            return parent.childes.get(pk=childe_id)

        if user.type == TEACHER_KEY_WORD:
            child = parent.childes.get(pk=childe_id)
            if child.kelaases.filter(teacher_id=user.id).exists():
                return child

    except Student.DoesNotExist:
        raise HamkelaasyError(4046)

    raise HamkelaasyError(4032)


def teacher__get_kelaases(teacher, user):
    if not user.id == teacher.id:
        raise HamkelaasyError(4032)

    return teacher.kelaases.all().order_by('-id')


def teacher__get_kelaas(teacher, user, kelaas_id):
    if not user.id == teacher.id:
        raise HamkelaasyError(4032)

    try:
        return teacher.kelaases.get(pk=kelaas_id)
    except Kelaas.DoesNotExist:
        raise HamkelaasyError(4041)


def student__get_code(student, user):
    if student.id == user.id:
        return student.code
    raise HamkelaasyError(4032)


def student__get_kelaases(student, user):
    if user.id == student.id:
        if student.parents:
            return student.kelaases.all().order_by('-id')

    if user.type == TEACHER_KEY_WORD:
        return [kelaas for kelaas in student.kelaases.all() if
                user.teacher.kelaases.filter(id=kelaas.id).exists()].reverse()

    if user.type == PARENT_KEY_WORD and user.id == student.parents.id:
        return student.kelaases.all().order_by('-id')

    raise HamkelaasyError(4032)


def student__get_kelaas(student, user, kelaas_id):
    try:
        if user.id == student.id:
            if student.parents:
                return student.kelaases.get(pk=kelaas_id)

        if user.type == PARENT_KEY_WORD and user.id == student.parents.id:
            return student.kelaases.get(pk=kelaas_id)

        if user.type == TEACHER_KEY_WORD:
            if user.teacher.kelaases.filter(pk=kelaas_id).exists():
                return student.kelaases.get(pk=kelaas_id)
    except Kelaas.DoesNotExist:
        raise HamkelaasyError(4041)

    raise HamkelaasyError(4032)


def student__get_badges(student, user, **kwargs):
    if user.id == student.id:
        if student.parents:
            if 'kelaas_id' in kwargs:
                return student.badges.filter(kelaas_id=kwargs['kelaas_id'])
            return student.badges.all()

    if user.type == TEACHER_KEY_WORD:
        if 'kelaas_id' in kwargs:
            if user.teacher.kelaases.filter(id=kwargs['kelaas_id']).exists():
                return student.badges.filter(kelaas_id=kwargs['kelaas_id'])

        badges = []
        for kelaas in user.teacher.kelaases.all():
            if kelaas.students.filter(pk=student.id).exists():
                badges.extend(student.badges.filter(kelaas=kelaas))
        return badges

    if user.type == PARENT_KEY_WORD and user.id == student.parents.id:
        if 'kelaas_id' in kwargs:
            student.badges.filter(kelaas_id=kwargs['kelaas_id'])
        return student.badges.all()

    raise HamkelaasyError(4032)


def student__get_parent(student, user):
    if user.id == student.id:
        return student.parents

    if user.type == TEACHER_KEY_WORD:
        for kelaas in user.teacher.kelaases.all():
            if kelaas.students.filter(pk=student.id).exists():
                return student.parents

    if user.type == PARENT_KEY_WORD and user.id == student.parents.id:
        return student.parents

    raise HamkelaasyError(4032)


def kelaas__get_tags(kelaas):
    return kelaas.tags.all()


def kelaas__get_student(kelaas, user):
    if user.type == TEACHER_KEY_WORD:
        if teacher_has_access_to_kelaas(kelaas=kelaas, teacher=user.teacher):
            return kelaas.students.all()

    if user.type == PARENT_KEY_WORD:
        return kelaas.students.filter(parents_id=user.id)

    raise HamkelaasyError(4032)


def kelaas__get_kelaas_post(kelaas, user):
    if user.type == PARENT_KEY_WORD:
        raise HamkelaasyError(4032)

    if kelaas.students.filter(pk=user.id).exists() or teacher_has_access_to_kelaas(kelaas, user.teacher):
        return kelaas.posts.filter(type=KELAAS_POST_KEY_WORD).order_by('-id')

    raise HamkelaasyError(4032)


def kelaas_get_stories(kelaas, user):
    if user.type == TEACHER_KEY_WORD:
        if teacher_has_access_to_kelaas(kelaas, user.teacher):
            return kelaas.posts.filter(type=STORY_KEY_WORD).all().order_by('-id')

    if user.type == PARENT_KEY_WORD:
        if parent_has_access_to_kelaas(kelaas=kelaas, parent=user.parent):
            return kelaas.posts.filter(type=STORY_KEY_WORD).all().order_by('-id')

    raise HamkelaasyError(4032)


def kelaas__get_conversations(kelaas, user):
    return kelaas.conversations.filter(members__id=user.id).order_by('-last_message_time')


def kelaas__get_conversation(kelaas, user, conversation_id):
    if kelaas.conversations.filter(members__id=user.id, id=conversation_id).exists():
        return kelaas.conversations.filter(members__id=user.id, id=conversation_id).first()

    raise HamkelaasyError(4045)


def kelaas__get_invite_code(kelaas, user):
    if user.type == TEACHER_KEY_WORD:
        if teacher_has_access_to_kelaas(kelaas, user.teacher):
            return kelaas.invite_code

    if user.type == STUDENT_KEY_WORD:
        if user.student.kelaases.filter(pk=kelaas.id).exists():
            return kelaas.invite_code

    # TODO why pass invite code to parent?!!!!
    if user.type == PARENT_KEY_WORD:
        if parent_has_access_to_kelaas(kelaas=kelaas, parent=user.parent):
            return kelaas.invite_code

    raise HamkelaasyError(4032)


def post__get_comments(post, user):
    # TODO permission checking
    return post.comments.all().order_by('-id')


def post__get_comments_count(post, user):
    # type: (Post, Person) -> int
    # TODO permission checking
    return post.comments.count()


def story__get_likes_count(story, user):
    # TODO permission checking
    return story.like_count


def kelaas_post__get_files(kelaas_post, user):
    # TODO permission checking
    return kelaas_post.files.all()


def conversation__get_messages(conversation, user):
    # TODO permission checking
    return conversation.messages.all().order_by('-id')


def conversation__get_last_message(conversation, user):
    # TODO permissopn checking
    return conversation.messages.all().last()


def messages__is_my_message(message, user):
    if user.id == message.writer.id:
        return True
    return False


def certificate__get_levels(certificate, user=None):
    return certificate.levels.all()


def is_my_comment(user, comment):
    if comment.owner.id == user.id:
        return True
    return False


# ______________________________________________________________________________________________________
# ______________________________________________________________________________________________________

def create_kelaas(user, title, description, gender, tags):
    if not user.type == TEACHER_KEY_WORD:
        raise HamkelaasyError(4032)

    kelaas = Kelaas(
        title=title,
        description=description,
        teacher=user.teacher,
        gender=gender
    )
    kelaas.save()

    for tag_id in tags.split(','):
        try:
            tagid = int(tag_id)
            if Tag.objects.filter(pk=tagid).exists():
                tag = Tag.objects.get(pk=tagid)
                kelaas.tags.add(tag)
        except ValueError:
            pass
    kelaas.save()

    return kelaas


def add_child(user, child_code):
    if not user.type == PARENT_KEY_WORD:
        raise HamkelaasyError(4032)

    try:
        student = Student.objects.get(code=child_code)
        if student.parents and student.parents.id == user.id:
            return student
        if student.parents:
            raise HamkelaasyError(4032)

        student.parents = user.parent
        student.save()
    except Student.DoesNotExist:
        raise HamkelaasyError(4042)

    for kelaas in student.kelaases.all():
        create_dialog(
            user=user.parent,
            kelaas_id=kelaas.id,
            interlocutor_id=kelaas.teacher.id
        )
    return student


def add_child_by_token(user, child_token):
    if not user.type == PARENT_KEY_WORD:
        raise HamkelaasyError(4032)

    try:
        temp = Token.objects.get(key=child_token)
        student = temp.user.person.student
        if student.parents:
            raise HamkelaasyError(4032)

        student.parents = user.parent
        student.save()
    except AttributeError:
        raise HamkelaasyError(4042)

    for kelaas in student.kelaases.all():
        create_dialog(
            user=user.parent,
            kelaas_id=kelaas.id,
            interlocutor_id=kelaas.teacher.id
        )
    return student


def add_comment(user, post_id, body):
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        raise HamkelaasyError(4047)

    if user.type == STUDENT_KEY_WORD:
        if not user.student.kelaases.filter(pk=post.kelaas_id).exists():
            raise HamkelaasyError(4032)

    if user.type == TEACHER_KEY_WORD:
        if not user.teacher.kelaases.filter(pk=post.kelaas_id).exists():
            raise HamkelaasyError(4032)

    if user.type == PARENT_KEY_WORD:
        access_flag = False
        for student in user.parent.childes.all():
            if student.kelaases.filter(pk=post.kelaas_id).exists():
                access_flag = True
                break
        if not access_flag:
            raise HamkelaasyError(4032)

    comment = Comment(
        body=body,
        post_id=post_id,
        owner_id=user.id,
    )
    comment.save()
    return comment


def delete_comment(user, comment_id):
    try:
        comment = Comment.objects.get(id=comment_id)
        if comment.owner_id == user.id:
            comment.delete()
            return

        if user.type == TEACHER_KEY_WORD:
            if teacher_has_access_to_kelaas(kelaas=comment.post.kelaas, teacher=user.teacher):
                comment.delete()
                return

        raise HamkelaasyError(4032)
    except Comment.DoesNotExist:
        raise HamkelaasyError(4052)


def assign_badge(user, kelaas_id, student_id, badges):
    if not user.type == TEACHER_KEY_WORD:
        raise HamkelaasyError(4032)
    teacher = user.teacher

    if not teacher.kelaases.filter(pk=kelaas_id).exists():
        return False
    try:
        kelaas = user.teacher.kelaases.get(pk=kelaas_id)
        student = Student.objects.get(pk=student_id)
    except Kelaas.DoesNotExist:
        raise HamkelaasyError(4041)
    except Student.DoesNotExist:
        raise HamkelaasyError(4042)

    for badge_id in badges.split(','):
        if Badge_link.objects.filter(student=student, type_id=badge_id, kelaas=kelaas).exists():
            badge_link = Badge_link.objects.filter(student=student, type_id=badge_id, kelaas=kelaas).first()
            badge_link.count = badge_link.count + 1
            badge_link.save()
        else:
            if not Badge.objects.filter(pk=badge_id).exists():
                raise HamkelaasyError(4048)
            badge_link = Badge_link(
                student=student,
                kelaas=kelaas,
                type_id=badge_id,
            )
            badge_link.save()
    return badge_link


def create_kelaas_post(user, kelaas_id, title, description, files):
    if not user.type == TEACHER_KEY_WORD:
        raise HamkelaasyError(4032)

    try:
        kelaas = user.teacher.kelaases.get(pk=kelaas_id)
    except Kelaas.DoesNotExist:
        raise HamkelaasyError(4041)

    post = Kelaas_post(
        title=title,
        description=description,
        kelaas=kelaas,
        owner=user.teacher,
    )
    post.save()

    for file_id in files.split(','):
        try:
            fid = int(file_id)
            if File.objects.filter(pk=fid).exists():
                input_file = File.objects.get(pk=file_id)
                post.files.add(input_file)
        except ValueError:
            pass
    post.save()

    return post


def delete_post(user, post_id):
    if not user.type == TEACHER_KEY_WORD:
        raise HamkelaasyError(4032)

    try:
        post = Post.objects.get(id=post_id)
        if not teacher_has_access_to_kelaas(kelaas=post.kelaas, teacher=user.teacher):
            raise HamkelaasyError(4032)

        post.delete()
    except Post.DoesNotExist:
        raise HamkelaasyError(4047)


def create_story(user, kelaas_id, title, description, pic_id=None):
    if not user.type == TEACHER_KEY_WORD:
        raise HamkelaasyError(4032)

    try:
        kelaas = user.teacher.kelaases.get(pk=kelaas_id)
    except Kelaas.DoesNotExist:
        raise HamkelaasyError(4041)

    story = Story(
        title=title,
        description=description,
        kelaas=kelaas,
        owner=user.teacher,
    )
    story.save()

    if pic_id:
        if File.objects.filter(pk=pic_id).exists():
            story.story_pic_id = pic_id
    story.save()
    return story


def join_kelaas_for_parent(user, invite_code, student_id):
    if not user.type == PARENT_KEY_WORD:
        raise HamkelaasyError(4032)

    try:
        student = Student.objects.get(id=student_id)
        if not student.parents.id == user.id:
            raise HamkelaasyError(4032)

        return join_kelaas(user=student, invite_code=invite_code)

    except Student.DoesNotExist:
        raise HamkelaasyError(4041)


def join_kelaas(user, invite_code):
    if not user.type == STUDENT_KEY_WORD:
        raise HamkelaasyError(4032)

    invite_code = invite_code.upper()
    try:
        kelaas = Kelaas.objects.get(invite_code=invite_code)
    except Kelaas.DoesNotExist:
        raise HamkelaasyError(4041)

    if kelaas.gender != 2 and kelaas.gender != user.student.gender:
        raise HamkelaasyError(4007)

    if not kelaas.students.filter(pk=user.id).exists():
        kelaas.students.add(user.student)
        kelaas.save()

    if user.student.parents:
        create_dialog(
            user=user.student.parents,
            kelaas_id=kelaas.id,
            interlocutor_id=kelaas.teacher.id
        )

    return kelaas


def send_message(user, conversation_id, message):
    try:
        conversation = Conversation.objects.get(pk=conversation_id)
    except Conversation.DoesNotExist:
        raise HamkelaasyError(4045)

    if not conversation.members.filter(pk=user.id).exists():
        raise HamkelaasyError(4032)

    msg = Conversation_message(
        writer=user,
        body=message,
        conversation_id=conversation_id
    )
    msg.save()
    return msg


def assign_certificate(user, type_id, level, owner_id, ):
    try:
        certificate_level = Certificate.objects.get(pk=type_id).levels.filter(level=level).first()
        owner = Person.objects.get(pk=owner_id)

        if not user.type == TEACHER_KEY_WORD:
            raise HamkelaasyError(4032)

        if not user.teacher.kelaases.filter(students__in=[owner.id]).exists():
            raise HamkelaasyError(4032)

        # TODO continuously levels checking
        # TODO same certificate level from different persons!!!

        if owner.certificates.filter(certificate_level=certificate_level, assigner_id=user.id).exists():
            return owner.certificates.filter(certificate_level=certificate_level, assigner_id=user.id).first()

        certificate_link = Certificate_link(
            certificate_level=certificate_level,
            owner=owner,
            assigner=user
        )
        certificate_link.save()
        return certificate_link

    except Certificate.DoesNotExist:
        raise HamkelaasyError(4044)
    except Person.DoesNotExist:
        raise HamkelaasyError(4049)


def create_certificate(user, title, description):
    # TODO permission check!!
    # TODO duplicate certificate?

    if user.created_certificates.filter(title=title).exists():
        raise HamkelaasyError(4008)

    certificate = Certificate(
        title=title,
        description=description,
        creator=user
    )
    certificate.save()
    return certificate


def create_certificate_level(user, certificate_id, level, level_description):
    # TODO permission checking
    try:
        certificate = Certificate.objects.get(pk=certificate_id)
    except Certificate.DoesNotExist:
        raise HamkelaasyError(4044)

    if not user.id == certificate.creator.id:
        raise HamkelaasyError(4032)

    if certificate.levels.filter(level=level).exists():
        raise HamkelaasyError(4009)

    certi_level = Certificate_level(
        level=level,
        level_description=level_description,
        type=certificate,
    )
    certi_level.save()
    return certi_level


def create_dialog(user, kelaas_id, interlocutor_id):
    # TODO permission denied!!
    try:
        kelaas = Kelaas.objects.get(pk=kelaas_id)
        partner = Person.objects.get(id=interlocutor_id)

        for conv in kelaas.conversations.filter(type=DIALOG_KEY_WORD):
            if conv.conversation_dialog.has_same_users(user1=user, user2=partner):
                return conv

        conversation = Conversation_dialog(kelaas_id=kelaas.id)
        conversation.save()

        conversation.members.add(user)
        conversation.members.add(partner)
        conversation.save()
        return conversation

    except Person.DoesNotExist:
        raise HamkelaasyError(4050)
    except Kelaas.DoesNotExist:
        raise HamkelaasyError(4041)


def perform_task(user, task_id):
    try:
        task = Task.objects.get(pk=task_id)
        if not task.student_id == user.id:
            raise HamkelaasyError(4032)

        task.is_done = Task
        task.save()
        return task

    except Task.DoesNotExist:
        raise HamkelaasyError(5051)
