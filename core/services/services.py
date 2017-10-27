import exceptions as exceptions
import logging

import make_notification as notification

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
frequent_logger = logging.getLogger('frequent_core')

DEFAULT_PAGE_SIZE = 10
MAX_PAGE_SIZE = 100


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


def parent_has_access_to_kelaas(kelaas, parent):
    frequent_logger.debug('parent_has_access_to_kelaas')

    for student in parent.childes.all():
        if kelaas.students.filter(pk=student.id).exists():
            return True
    return False


def teacher_has_access_to_kelaas(kelaas, teacher):
    frequent_logger.debug('teacher_has_access_to_kelaas')
    if kelaas.teacher.id == teacher.id:
        return True
    return False


# ______________________________________________________________________________________________________
# ______________________________________________________________________________________________________

def get_not_seen_notification_count(user, person):
    frequent_logger.debug('get_not_seen_notification_count')

    if user.id == person.id:
        return user.notifications.filter(has_seen=False).count()

    raise HamkelaasyError(Error_code.Authentication.Permission_denied)


def get_notifications(user, seen_notification=False, get_all=False):
    frequent_logger.debug('get_notifications')

    if not seen_notification:
        return user.notifications.filter(has_seen=False)
    if get_all:
        return user.notifications.all()

    return user.notifications.filter(has_seen=True)


def get_kelaas_by_invite_code(invite_code):
    frequent_logger.debug('get_kelaas_by_invite_code')

    try:
        return Kelaas.objects.get(invite_code=invite_code)
    except Kelaas.DoesNotExist:
        raise HamkelaasyError(Error_code.Object_not_found.Kelaas)


def get_student(user, **kwargs):
    frequent_logger.debug('get_student')

    if user.type == STUDENT_KEY_WORD:
        return user.student

    if not 'id' in kwargs:
        raise HamkelaasyError(Error_code.Student.Id_required)
    id = kwargs['id']

    if user.type == PARENT_KEY_WORD:
        try:
            return user.parent.childes.get(pk=id)
        except Student.DoesNotExist:
            raise HamkelaasyError(Error_code.Object_not_found.Student)

    if user.type == TEACHER_KEY_WORD:
        for teacher_kelaas in user.teacher.kelaases.all():
            if teacher_kelaas.students.filter(pk=id).exists():
                return teacher_kelaas.students.get(pk=id)
        raise HamkelaasyError(Error_code.Object_not_found.Student)


def get_students(user, **kwargs):
    frequent_logger.debug('get_students')

    if user.type == PARENT_KEY_WORD:
        return user.parent.childes.all()

    if user.type == TEACHER_KEY_WORD:
        if 'kelaas_id' in kwargs:
            try:
                return Kelaas.objects.get(pk=kwargs['kelaas_id']).students.all()
            except Kelaas.DoesNotExist:
                raise HamkelaasyError(Error_code.Object_not_found.Kelaas)
        raise HamkelaasyError(Error_code.Kelaas.Id_required)

    raise HamkelaasyError(Error_code.Authentication.Permission_denied)


def get_kelaas(user, kelaas_id):
    frequent_logger.debug('get_kelaas')

    if user.type == TEACHER_KEY_WORD:
        try:
            return user.teacher.kelaases.get(pk=kelaas_id)
        except Kelaas.DoesNotExist:
            raise HamkelaasyError(Error_code.Object_not_found.Kelaas)

    if user.type == PARENT_KEY_WORD:
        for student in user.parent.childes.all():
            if student.kelaases.filter(pk=kelaas_id).exists():
                return student.kelaases.get(pk=kelaas_id)
        raise HamkelaasyError(Error_code.Object_not_found.Kelaas)

    if user.type == STUDENT_KEY_WORD:
        try:
            return user.student.kelaases.get(pk=kelaas_id)
        except Kelaas.DoesNotExist:
            raise HamkelaasyError(Error_code.Object_not_found.Kelaas)

    raise HamkelaasyError(Error_code.Authentication.Permission_denied)


def get_kelaases(user, **kwargs):
    frequent_logger.debug('get_kelaases')

    if user.type == TEACHER_KEY_WORD:
        return user.teacher.kelaases.all()

    if user.type == PARENT_KEY_WORD:
        try:
            return user.parent.childes.get(pk=kwargs['student_id']).kelaases.all()
        except exceptions.KeyError:
            raise HamkelaasyError(Error_code.Student.Id_required)
        except Student.DoesNotExist:
            raise HamkelaasyError(Error_code.Object_not_found.Student)

    if user.type == STUDENT_KEY_WORD:
        return user.student.kelaases.all()

    raise HamkelaasyError(Error_code.Authentication.Permission_denied)


def get_teacher(user):
    frequent_logger.debug('get_teacher')

    if user.type == TEACHER_KEY_WORD:
        return user.teacher

    raise HamkelaasyError(Error_code.Authentication.Only_teacher)


def get_parent(user, **kwargs):
    frequent_logger.debug('get_parent')

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
            raise HamkelaasyError(Error_code.Object_not_found.Parent)
        except exceptions.KeyError:
            raise HamkelaasyError(Error_code.Parent.Id_required)

    raise HamkelaasyError(Error_code.Authentication.Permission_denied)


def get_badge_types(**kwargs):
    frequent_logger.debug('get_badge_types')

    if 'id' in kwargs:
        id = kwargs['id']
        return Badge.objects.get(pk=id)

    return Badge.objects.all()


def get_certificate(id):
    frequent_logger.debug('get_certificate')

    try:
        return Certificate.objects.get(pk=id)
    except Certificate.DoesNotExist:
        raise HamkelaasyError(Error_code.Object_not_found.Certificate)


def get_tags():
    frequent_logger.debug('get_tags')

    return Tag.objects.all()


def get_conversation(user, conversation_id):
    frequent_logger.debug('get_conversation')

    try:
        conversation = Conversation.objects.get(pk=conversation_id)
        if conversation.members.filter(id=user.id).exists():
            return conversation
    except Conversation.DoesNotExist:
        raise HamkelaasyError(Error_code.Object_not_found.Conversation)

    raise HamkelaasyError(Error_code.Certificate.Permisson_denied)


def get_system_notifications(user, new=False):
    frequent_logger.debug('get_system_notifications')

    # TODO show system notification for each user type
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


def get_parent_childes(parent, user, **kwargs):
    frequent_logger.debug('get_parent_childes')

    if parent.id == user.id:
        return parent.childes.all()

    if user.type == TEACHER_KEY_WORD:
        if 'kelaas_id' in kwargs:
            if user.teacher.kelaases.filter(pk=kwargs['kelaas_id']).exists():
                return parent.childes.filter(kelaases__in=[kwargs['kelaas_id']])
            return []

        result = []
        # user.kelaases.filter(students__in=[child.id for child in parent.childes.all()])
        for child in parent.childes.all():
            if child.kelaases.filter(teacher_id=user.id).exists():
                result.append(child)
        return result

    raise HamkelaasyError(Error_code.Student.Permission_denied)


def get_parent_child(parent, user, childe_id):
    frequent_logger.debug('get_parent_child')

    try:
        if parent.id == user.id:
            return parent.childes.get(pk=childe_id)

        if user.type == TEACHER_KEY_WORD:
            child = parent.childes.get(pk=childe_id)
            if child.kelaases.filter(teacher_id=user.id).exists():
                return child

    except Student.DoesNotExist:
        raise HamkelaasyError(Error_code.Object_not_found.Student)

    raise HamkelaasyError(Error_code.Student.Permission_denied)


def get_teacher_kelaases(teacher, user):
    frequent_logger.debug('get_teacher_kelaases')

    if not user.id == teacher.id:
        raise HamkelaasyError(Error_code.Authentication.Permission_denied)

    return teacher.kelaases.all().order_by('-id')


def get_teacher_kelaas(teacher, user, kelaas_id):
    frequent_logger.debug('get_teacher_kelaas')

    if not user.id == teacher.id:
        raise HamkelaasyError(Error_code.Authentication.Permission_denied)

    try:
        return teacher.kelaases.get(pk=kelaas_id)
    except Kelaas.DoesNotExist:
        raise HamkelaasyError(Error_code.Object_not_found.Kelaas)


def get_student_code(student, user):
    frequent_logger.debug('get_student_code')

    if student.id == user.id:
        return student.code
    if user.type == TEACHER_KEY_WORD:
        if user.teacher.kelaases.filter(students__in=[student.id]).exists():
            return student.code
    raise HamkelaasyError(Error_code.Authentication.Permission_denied)


def get_student_kelaases(student, user):
    frequent_logger.debug('get_student_kelaases')

    if user.id == student.id:
        if student.parents:
            return student.kelaases.all().order_by('-id')
        return []

    if user.type == TEACHER_KEY_WORD:
        return [kelaas for kelaas in student.kelaases.all() if
                user.teacher.kelaases.filter(id=kelaas.id).exists()].reverse()

    if user.type == PARENT_KEY_WORD and user.id == student.parents.id:
        return student.kelaases.all().order_by('-id')

    raise HamkelaasyError(Error_code.Authentication.Permission_denied)


def get_student_kelaas(student, user, kelaas_id):
    frequent_logger.debug('get_student_kelaas')

    try:
        if user.id == student.id:
            if student.parents:
                return student.kelaases.get(pk=kelaas_id)
            return

        if user.type == PARENT_KEY_WORD and user.id == student.parents.id:
            return student.kelaases.get(pk=kelaas_id)

        if user.type == TEACHER_KEY_WORD:
            if user.teacher.kelaases.filter(pk=kelaas_id).exists():
                return student.kelaases.get(pk=kelaas_id)
    except Kelaas.DoesNotExist:
        raise HamkelaasyError(Error_code.Object_not_found.Kelaas)

    raise HamkelaasyError(Error_code.Authentication.Permission_denied)


def get_student_badges(student, user, **kwargs):
    frequent_logger.debug('get_student_badges')

    if user.id == student.id:
        if student.parents:
            if 'kelaas_id' in kwargs:
                return student.badges.filter(kelaas_id=kwargs['kelaas_id'])
            return student.badges.all()
        return []

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

    raise HamkelaasyError(Error_code.Authentication.Permission_denied)


def get_student_parent(student, user):
    frequent_logger.debug('get_student_parent')

    if user.id == student.id:
        return student.parents

    if user.type == TEACHER_KEY_WORD:
        for kelaas in user.teacher.kelaases.all():
            if kelaas.students.filter(pk=student.id).exists():
                return student.parents

    if user.type == PARENT_KEY_WORD and user.id == student.parents.id:
        return student.parents

    raise HamkelaasyError(Error_code.Authentication.Permission_denied)


def get_kelaas_tags(kelaas):
    frequent_logger.debug('get_kelaas_tags')

    return kelaas.tags.all()


def get_kelaas_students(kelaas, user):
    frequent_logger.debug('get_kelaas_students')

    if user.type == TEACHER_KEY_WORD:
        if teacher_has_access_to_kelaas(kelaas=kelaas, teacher=user.teacher):
            return kelaas.students.all()

    if user.type == PARENT_KEY_WORD:
        return kelaas.students.filter(parents_id=user.id)

    raise HamkelaasyError(Error_code.Authentication.Permission_denied)


def kelaas__get_kelaas_post(kelaas, user):
    frequent_logger.debug('kelaas__get_kelaas_post')

    if user.type == PARENT_KEY_WORD:
        raise HamkelaasyError(Error_code.Authentication.Permission_denied)

    if kelaas.students.filter(pk=user.id).exists() or teacher_has_access_to_kelaas(kelaas, user.teacher):
        return kelaas.posts.filter(type=KELAAS_POST_KEY_WORD).order_by('-id')

    raise HamkelaasyError(Error_code.Authentication.Permission_denied)


def kelaas_get_stories(kelaas, user):
    frequent_logger.debug('kelaas_get_stories')

    if user.type == TEACHER_KEY_WORD:
        if teacher_has_access_to_kelaas(kelaas, user.teacher):
            return kelaas.posts.filter(type=STORY_KEY_WORD).all().order_by('-id')

    if user.type == PARENT_KEY_WORD:
        if parent_has_access_to_kelaas(kelaas=kelaas, parent=user.parent):
            return kelaas.posts.filter(type=STORY_KEY_WORD).all().order_by('-id')

    raise HamkelaasyError(Error_code.Authentication.Permission_denied)


def kelaas__get_conversations(kelaas, user):
    frequent_logger.debug('kelaas__get_conversations')

    return kelaas.conversations.filter(members__id=user.id).order_by('-last_message_time')


def kelaas__get_conversation(kelaas, user, conversation_id):
    frequent_logger.debug('kelaas__get_conversation')

    if kelaas.conversations.filter(members__id=user.id, id=conversation_id).exists():
        return kelaas.conversations.filter(members__id=user.id, id=conversation_id).first()

    raise HamkelaasyError(Error_code.Object_not_found.Conversation)


def kelaas__get_invite_code(kelaas, user):
    frequent_logger.debug('kelaas__get_invite_code')

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

    raise HamkelaasyError(Error_code.Authentication.Permission_denied)


def post__get_comments(post, user):
    frequent_logger.debug('post__get_comments')

    # TODO permission checking
    return post.comments.all().order_by('-id')


def post__get_comments_count(post, user):
    frequent_logger.debug('post__get_comments_count')

    # TODO permission checking
    return post.comments.count()


def story__get_likes_count(story, user):
    frequent_logger.debug('story__get_likes_count')

    # TODO permission checking
    return story.like_count


def kelaas_post__get_files(kelaas_post, user):
    frequent_logger.debug('kelaas_post__get_files')

    # TODO permission checking
    return kelaas_post.files.all()


def conversation__get_messages(conversation, user):
    frequent_logger.debug('conversation__get_messages')

    # TODO permission checking
    return conversation.messages.all().order_by('-id')


def conversation__get_last_message(conversation, user):
    frequent_logger.debug('conversation__get_last_message')

    # TODO permissopn checking
    return conversation.messages.all().last()


def messages__is_my_message(message, user):
    frequent_logger.debug('messages__is_my_message')

    if user.id == message.writer.id:
        return True
    return False


def certificate__get_levels(certificate, user=None):
    frequent_logger.debug('certificate__get_levels')

    return certificate.levels.all()


def is_my_comment(user, comment):
    frequent_logger.debug('is_my_comment')

    if comment.owner.id == user.id:
        return True
    return False


# ______________________________________________________________________________________________________
# ______________________________________________________________________________________________________

def create_kelaas(user, title, description, gender, tags):
    frequent_logger.debug('create_kelaas')

    if not user.type == TEACHER_KEY_WORD:
        raise HamkelaasyError(Error_code.Authentication.Only_teacher)

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
    frequent_logger.debug('add_child')

    if not user.type == PARENT_KEY_WORD:
        raise HamkelaasyError(Error_code.Authentication.Only_parent)

    try:
        student = Student.objects.get(code=child_code)
        if student.parents and student.parents.id == user.id:
            return student
        if student.parents:
            raise HamkelaasyError(Error_code.Student.Has_parent)

        student.parents = user.parent
        student.my_save()
    except Student.DoesNotExist:
        raise HamkelaasyError(Error_code.Object_not_found.Student)

    for kelaas in student.kelaases.all():
        create_dialog(
            user=user.parent,
            kelaas_id=kelaas.id,
            interlocutor_id=kelaas.teacher.id
        )
    return student


def add_child_by_token(user, child_token):
    frequent_logger.debug('add_child_by_token')

    if not user.type == PARENT_KEY_WORD:
        raise HamkelaasyError(Error_code.Authentication.Only_parent)

    try:
        temp = Token.objects.get(key=child_token)
        student = temp.user.person.student
        if student.parents:
            raise HamkelaasyError(Error_code.Student.Has_parent)

        student.parents = user.parent
        student.my_save()
    except AttributeError:
        raise HamkelaasyError(Error_code.Object_not_found.Student)

    for kelaas in student.kelaases.all():
        create_dialog(
            user=user.parent,
            kelaas_id=kelaas.id,
            interlocutor_id=kelaas.teacher.id
        )
    return student


def add_comment(user, post_id, body):
    frequent_logger.debug('add_comment')

    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        raise HamkelaasyError(Error_code.Object_not_found.Post)

    if user.type == STUDENT_KEY_WORD:
        if not user.student.kelaases.filter(pk=post.kelaas_id).exists():
            raise HamkelaasyError(Error_code.Authentication.Permission_denied)

    if user.type == TEACHER_KEY_WORD:
        if not user.teacher.kelaases.filter(pk=post.kelaas_id).exists():
            raise HamkelaasyError(Error_code.Authentication.Permission_denied)

    if user.type == PARENT_KEY_WORD:
        access_flag = False
        for student in user.parent.childes.all():
            if student.kelaases.filter(pk=post.kelaas_id).exists():
                access_flag = True
                break
        if not access_flag:
            raise HamkelaasyError(Error_code.Authentication.Permission_denied)

    comment = Comment(
        body=body,
        post_id=post_id,
        owner_id=user.id,
    )
    comment.save()
    return comment


def delete_comment(user, comment_id):
    frequent_logger.debug('delete_comment')

    try:
        comment = Comment.objects.get(id=comment_id)
        if comment.owner_id == user.id:
            comment.delete()
            return

        if user.type == TEACHER_KEY_WORD:
            if teacher_has_access_to_kelaas(kelaas=comment.post.kelaas, teacher=user.teacher):
                comment.delete()
                return

        raise HamkelaasyError(Error_code.Authentication.Permission_denied)
    except Comment.DoesNotExist:
        raise HamkelaasyError(Error_code.Object_not_found.Comment)


def assign_badge(user, kelaas_id, student_id, badges):
    frequent_logger.debug('assign_badge')

    if not user.type == TEACHER_KEY_WORD:
        raise HamkelaasyError(Error_code.Authentication.Only_teacher)
    teacher = user.teacher

    if not teacher.kelaases.filter(pk=kelaas_id).exists():
        return False
    try:
        kelaas = user.teacher.kelaases.get(pk=kelaas_id)
        student = Student.objects.get(pk=student_id)
    except Kelaas.DoesNotExist:
        raise HamkelaasyError(Error_code.Object_not_found.Kelaas)
    except Student.DoesNotExist:
        raise HamkelaasyError(Error_code.Object_not_found.Student)

    for badge_id in badges.split(','):
        if Badge_link.objects.filter(student=student, type_id=badge_id, kelaas=kelaas).exists():
            badge_link = Badge_link.objects.filter(student=student, type_id=badge_id, kelaas=kelaas).first()
            badge_link.count = badge_link.count + 1
            badge_link.save()
        else:
            if not Badge.objects.filter(pk=badge_id).exists():
                raise HamkelaasyError(Error_code.Object_not_found.Badge)
            badge_link = Badge_link(
                student=student,
                kelaas=kelaas,
                type_id=badge_id,
            )
            badge_link.save()
    return badge_link


def create_kelaas_post(user, kelaas_id, title, description, files):
    frequent_logger.debug('create_kelaas_post')

    if not user.type == TEACHER_KEY_WORD:
        raise HamkelaasyError(Error_code.Authentication.Only_teacher)

    try:
        kelaas = user.teacher.kelaases.get(pk=kelaas_id)
    except Kelaas.DoesNotExist:
        raise HamkelaasyError(Error_code.Object_not_found.Kelaas)

    post = Kelaas_post(
        title=title,
        description=description,
        kelaas=kelaas,
        owner=user.teacher,
    )
    post.my_save()

    for file_id in files.split(','):
        try:
            fid = int(file_id)
            if File.objects.filter(pk=fid).exists():
                input_file = File.objects.get(pk=file_id)
                post.files.add(input_file)
        except ValueError:
            pass
    post.my_save()

    return post


def delete_post(user, post_id):
    frequent_logger.debug('delete_post')

    if not user.type == TEACHER_KEY_WORD:
        raise HamkelaasyError(Error_code.Authentication.Only_teacher)

    try:
        post = Post.objects.get(id=post_id)
        if not teacher_has_access_to_kelaas(kelaas=post.kelaas, teacher=user.teacher):
            raise HamkelaasyError(Error_code.Authentication.Permission_denied)

        post.delete()
    except Post.DoesNotExist:
        raise HamkelaasyError(Error_code.Object_not_found.Post)


def create_story(user, kelaas_id, title, description, pic_id=None):
    frequent_logger.debug('create_story')

    if not user.type == TEACHER_KEY_WORD:
        raise HamkelaasyError(Error_code.Authentication.Only_teacher)

    try:
        kelaas = user.teacher.kelaases.get(pk=kelaas_id)
    except Kelaas.DoesNotExist:
        raise HamkelaasyError(Error_code.Object_not_found.Kelaas)

    story = Story(
        title=title,
        description=description,
        kelaas=kelaas,
        owner=user.teacher,
    )
    story.my_save()

    if pic_id:
        if File.objects.filter(pk=pic_id).exists():
            story.story_pic_id = pic_id
    story.my_save()
    return story


def join_kelaas_by_parent(user, invite_code, student_id):
    frequent_logger.debug('join_kelaas_by_parent')

    if not user.type == PARENT_KEY_WORD:
        raise HamkelaasyError(Error_code.Authentication.Only_parent)

    try:
        student = Student.objects.get(id=student_id)
        if not student.parents.id == user.id:
            raise HamkelaasyError(Error_code.Authentication.Permission_denied)

        kelaas = join_kelaas_using_invite_code(user=student, invite_code=invite_code)
        notification.join_kelaas_by_parent(student=student, kelaas=kelaas)
        return kelaas

    except Student.DoesNotExist:
        raise HamkelaasyError(Error_code.Object_not_found.Student)


def join_kelaas_by_student(user, invite_code):
    frequent_logger.debug('join_kelaas_by_student')
    kelaas = join_kelaas_using_invite_code(user=user, invite_code=invite_code)
    notification.join_kelaas_by_student(student=user, kelaas=kelaas)
    return kelaas


def join_kelaas_using_invite_code(user, invite_code):
    frequent_logger.debug('join_kelaas_using_invite_code')

    invite_code = invite_code.upper()
    try:
        kelaas = Kelaas.objects.get(invite_code=invite_code)
        return join_kelaas(user=user, kelaas=kelaas)
    except Kelaas.DoesNotExist:
        raise HamkelaasyError(Error_code.Object_not_found.Kelaas)


def join_kelaas(user, kelaas):
    frequent_logger.debug('join_kelaas')

    if not user.type == STUDENT_KEY_WORD:
        raise HamkelaasyError(Error_code.Authentication.Only_student)

    if kelaas.gender != 2 and kelaas.gender != user.student.gender:
        raise HamkelaasyError(Error_code.Kelaas.Gender_doesnt_match)

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
    frequent_logger.debug('send_message')

    try:
        conversation = Conversation.objects.get(pk=conversation_id)
    except Conversation.DoesNotExist:
        raise HamkelaasyError(Error_code.Object_not_found.Conversation)

    if not conversation.members.filter(pk=user.id).exists():
        raise HamkelaasyError(Error_code.Authentication.Permission_denied)

    msg = Conversation_message(
        writer=user,
        body=message,
        conversation_id=conversation_id
    )
    msg.save()
    return msg


def assign_certificate(user, type_id, level, owner_id):
    frequent_logger.debug('assign_certificate')

    if not user.type == TEACHER_KEY_WORD:
        raise HamkelaasyError(Error_code.Authentication.Only_teacher)

    try:
        certificate_level = Certificate.objects.get(pk=type_id).levels.filter(level=level).first()
        owner = Person.objects.get(pk=owner_id)

        if not user.teacher.kelaases.filter(students__in=[owner.id]).exists():
            raise HamkelaasyError(Error_code.Authentication.Permission_denied)

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
        raise HamkelaasyError(Error_code.Object_not_found.Certificate)
    except Person.DoesNotExist:
        raise HamkelaasyError(Error_code.Object_not_found.Person)


def create_certificate(user, title, description):
    frequent_logger.debug('create_certificate')

    # TODO permission check!!
    # TODO duplicate certificate?

    if user.created_certificates.filter(title=title).exists():
        raise HamkelaasyError(Error_code.Certificate.Duplicate_title)

    certificate = Certificate(
        title=title,
        description=description,
        creator=user
    )
    certificate.save()
    return certificate


def create_certificate_level(user, certificate_id, level, level_description):
    frequent_logger.debug('create_certificate_level')

    # TODO permission checking
    try:
        certificate = Certificate.objects.get(pk=certificate_id)
    except Certificate.DoesNotExist:
        raise HamkelaasyError(Error_code.Object_not_found.Certificate)

    if not user.id == certificate.creator.id:
        raise HamkelaasyError(Error_code.Authentication.Permission_denied)

    if certificate.levels.filter(level=level).exists():
        raise HamkelaasyError(Error_code.Certificate.Duplicate_level)

    certi_level = Certificate_level(
        level=level,
        level_description=level_description,
        type=certificate,
    )
    certi_level.save()
    return certi_level


def create_dialog(user, kelaas_id, interlocutor_id):
    frequent_logger.debug('create_dialog')

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
        raise HamkelaasyError(Error_code.Object_not_found.Person)
    except Kelaas.DoesNotExist:
        raise HamkelaasyError(Error_code.Object_not_found.Kelaas)


def perform_task(user, task_id):
    frequent_logger.debug('perform_task')

    try:
        task = Task.objects.get(pk=task_id)
        if not task.student_id == user.id:
            raise HamkelaasyError(Error_code.Authentication.Permission_denied)

        task.is_done = Task
        task.save()
        return task

    except Task.DoesNotExist:
        raise HamkelaasyError(Error_code.Object_not_found.Task)


def remove_conversation_dialog(kelaas_id, user1_id, user2_id):
    frequent_logger.debug('remove_conversation_dialog')

    try:
        kelaas = Kelaas.objects.get(id=kelaas_id)
        u1 = Person.objects.get(id=user1_id)
        u2 = Person.objects.get(id=user2_id)

        for conv in kelaas.conversations.filter(type=DIALOG_KEY_WORD):
            if conv.conversation_dialog.has_same_users(user1=u1, user2=u2):
                conv.delete()
                return

    except Kelaas.DoesNotExist:
        raise HamkelaasyError(Error_code.Object_not_found.Kelaas)


def remove_student_from_kelaas(user, student_id, kelaas_id):
    frequent_logger.debug('remove_student_from_kelaas')

    if not user.type == TEACHER_KEY_WORD:
        raise HamkelaasyError(Error_code.Authentication.Only_teacher)

    try:
        kelaas = user.teacher.kelaases.get(id=kelaas_id)
        if not kelaas.students.filter(id=student_id).exists():
            raise HamkelaasyError(Error_code.Object_not_found.Student)

        student = kelaas.students.get(id=student_id)

        if student.parents:
            # TODO : check it for buggs
            if kelaas.students.filter(parents_id=student.parents.id).count() == 1:
                remove_conversation_dialog(kelaas_id, user.id, student.parents.id)

        kelaas.students.remove(student)

    except Kelaas.DoesNotExist:
        raise HamkelaasyError(Error_code.Object_not_found.Kelaas)
    except Student.DoesNotExist:
        raise HamkelaasyError(Error_code.Object_not_found.Student)


def make_notification_seen(user, notification_id):
    frequent_logger.debug('make_notification_seen')

    try:
        notification = Notification.objects.get(pk=notification_id)
        if not user.id == notification.receiver_id:
            raise HamkelaasyError(Error_code.Authentication.Permission_denied)

        notification.has_seen = True
        notification.save()
        return notification
    except Notification.DoesNotExist:
        raise HamkelaasyError(Error_code.Object_not_found.Notification)
