from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from core import myGraphQLError
from core.models import Parent, TEACHER_KEY_WORD, PARENT_KEY_WORD, Kelaas, KELAAS_POST_KEY_WORD, STORY_KEY_WORD, \
    STUDENT_KEY_WORD, Post, Person, Student

DEFAULT_PAGE_SIZE = 10


def apply_pagination(input_list, page=1, page_size=DEFAULT_PAGE_SIZE):
    paginator = Paginator(input_list, page_size)

    try:
        res = paginator.page(page)
    except PageNotAnInteger:
        res = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        res = paginator.page(paginator.num_pages)

    return res


def parent_has_access_to_kelaas(kelaas, parent):
    for student in parent.childes.all():
        if kelaas.students.filter(pk=student.id).exists():
            return True
    return False


def teacher_has_access_to_kelaas(kelaas, teacher):
    if kelaas.teachers.filter(pk=teacher.id).exists():
        return True
    return False


def parent__get_childes(parent, user, **kwargs):
    # type: (Parent, Person) -> object
    if parent.id == user.id:
        return parent.childes.all()

    if user.type == TEACHER_KEY_WORD:
        if 'kelaas_id' in kwargs:
            if user.kelaases.filter(kelaas_id=kwargs['kelaas_id']).exist():
                return parent.childes.filter(kelaases__in=[kwargs['kelaas_id']])
            raise myGraphQLError('Permission denied', status=403)

        result = []
        # user.kelaases.filter(students__in=[child.id for child in parent.childes.all()])
        for child in parent.childes.all():
            if child.kelaases.filter(teachers__in=[user.id]).exists():
                result.append(child)
        return result

    raise myGraphQLError('Permission denied', status=403)


def parent__get_child(parent, user, childe_id):
    try:
        if parent.id == user.id:
            return parent.childes.get(pk=childe_id)

        if user.type == TEACHER_KEY_WORD:
            child = parent.childes.get(pk=childe_id)
            if child.kelaases.filter(teachers__in=[user.id]).exists():
                return child

    except Student.DoesNotExist:
        raise myGraphQLError('Child not found', status=404)

    raise myGraphQLError('Permission denied', status=403)


def teacher__get_kelaases(teacher, user):
    if not user.id == teacher.id:
        raise myGraphQLError('Permission denied', status=403)

    return teacher.kelaases.all().order_by('-id')


def teacher__get_kelaas(teacher, user, kelaas_id):
    if not user.id == teacher.id:
        raise myGraphQLError('Permission denied', status=403)

    try:
        return teacher.kelaases.get(pk=kelaas_id)
    except Kelaas.DoesNotExist:
        raise myGraphQLError('Kelaas not found', status=404)


def student__get_invite_code(student, user):
    if student.id == user.id:
        return student.parent_cod
    raise myGraphQLError('Permission denied', status=403)


def student__get_kelaases(student, user):
    if user.id == student.id:
        return student.kelaases.all().order_by('-id')

    if user.type == TEACHER_KEY_WORD:
        return [kelaas for kelaas in student.kelaases.all() if
                user.teacher.kelaases.filter(id=kelaas.id).exists()].reverse()

    if user.type == PARENT_KEY_WORD and user.id == student.parents.id:
        return student.kelaases.all().order_by('-id')

    raise myGraphQLError('Permission denied', status=403)


def student__get_kelaas(student, user, kelaas_id):
    try:
        if user.id == student.id:
            return student.kelaases.get(pk=kelaas_id)

        if user.type == PARENT_KEY_WORD and user.id == student.parents.id:
            return student.kelaases.get(pk=kelaas_id)

        if user.type == TEACHER_KEY_WORD:
            if user.teacher.kelaases.filter(pk=kelaas_id).exists():
                return student.kelaases.get(pk=kelaas_id)
    except Kelaas.DoesNotExist:
        raise myGraphQLError('Kelaas not found', status=404)

    raise myGraphQLError('Permission denied', status=403)


def student__get_badges(student, user, **kwargs):
    if user.id == student.id:
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

    raise myGraphQLError('Permission denied', status=403)


def student__get_parent(student, user):
    if user.id == student.id:
        return student.parents

    if user.type == TEACHER_KEY_WORD:
        for kelaas in user.teacher.kelaases.all():
            if kelaas.students.filter(pk=student.id).exists():
                return student.parents

    if user.type == PARENT_KEY_WORD and user.id == student.parents.id:
        return student.parents

    raise myGraphQLError('Permission denied', status=403)


def kelaas__get_tags(kelaas):
    return kelaas.tags.all()


def kelaas__get_student(kelaas, user):
    if user.type == TEACHER_KEY_WORD:
        if teacher_has_access_to_kelaas(kelaas=kelaas, teacher=user.teacher):
            return kelaas.students.all()

    if user.type == PARENT_KEY_WORD:
        return kelaas.students.filter(parents_id=user.id)

    raise myGraphQLError('Permission denied', status=403)


def kelaas__get_kelaas_post(kelaas, user):
    if teacher_has_access_to_kelaas(kelaas, user.teacher) or kelaas.students.filter(pk=user.id).exists():
        return kelaas.posts.filter(type=KELAAS_POST_KEY_WORD).order_by('-id')

    raise myGraphQLError('Permission denied', status=403)


def kelaas_get_stories(kelaas, user):
    if user.type == TEACHER_KEY_WORD:
        if teacher_has_access_to_kelaas(kelaas, user.teacher):
            return kelaas.posts.filter(type=STORY_KEY_WORD).all().order_by('-id')

    if user.type == PARENT_KEY_WORD:
        if parent_has_access_to_kelaas(kelaas=kelaas, parent=user.parent):
            return kelaas.posts.filter(type=STORY_KEY_WORD).all().order_by('-id')

    raise myGraphQLError('Permission denied', status=403)


def kelaas__get_conversations(kelaas, user):
    return kelaas.conversations.filter(members__id=user.id).order_by('-last_message_time')


def kelaas__get_conversation(kelaas, user, conversation_id):
    # TODO exception handling(in case of invalid id)
    return kelaas.conversations.filter(members__id=user.id, id=conversation_id).first()


def kelaas__get_invite_code(kelaas, user):
    # type: (Kelaas, Person) -> string
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

    raise myGraphQLError('Permission denied', status=403)


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
