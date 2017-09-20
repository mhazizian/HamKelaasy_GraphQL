from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from core import myGraphQLError
from core.models import Parent

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
    except:
        raise myGraphQLError('Kelaas not found', status=404)
