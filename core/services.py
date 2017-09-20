from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from core import myGraphQLError
from core.models import Parent, TEACHER_KEY_WORD, PARENT_KEY_WORD, Kelaas

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


def parent__get_childes(parent, user):
    if not parent.id == user.id:
        raise myGraphQLError('Permission denied', status=403)

    return parent.childes.all()


def parent__get_child(parent, user, childe_id):
    if not parent.id == user.id:
        raise myGraphQLError('Permission denied', status=403)

    try:
        return parent.childes.get(pk=childe_id)
    except Parent.DoesNotExist:
        raise myGraphQLError('Child not found', status=404)


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
