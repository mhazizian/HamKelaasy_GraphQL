from graphql import GraphQLError


def it_is_him(obj1, obj2):
    if not obj1.id == obj2.id:
        raise GraphQLError('Permission denied')
    return True


def parent_has_access_to_kelaas(kelaas, parent):
    for student in parent.student_set.all():
        if kelaas.students.filter(pk=student.id).exists():
            return True
    return False