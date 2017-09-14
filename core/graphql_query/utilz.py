from core import myGraphQLError

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
