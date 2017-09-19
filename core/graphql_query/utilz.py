from core import myGraphQLError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

DEFAULT_PAGE_SIZE = 10


def it_is_him(obj1, obj2):
    if not obj1.id == obj2.id:
        return False
    return True


def parent_has_access_to_kelaas(kelaas, parent):
    for student in parent.childes.all():
        if kelaas.students.filter(pk=student.id).exists():
            return True
    return False


def teacher_has_access_to_kelaas(kelaas, teacher):
    if kelaas.teachers.filter(pk=teacher.id).exists():
        return True
    return False


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
