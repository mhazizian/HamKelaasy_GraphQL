import exceptions
import graphene

from core import myGraphQLError
from core.models import *
from graphql_query import *


def resolve_student(root, info, **kwargs):
    if not info.context.user.is_authenticated:
        raise myGraphQLError('user not authenticated', status=401)
    user = info.context.user.person

    if user.type == STUDENT_KEY_WORD:
        return user.student

    if not 'id' in kwargs:
        raise myGraphQLError('"id" is necessary', status=400)
    id = kwargs['id']

    if user.type == PARENT_KEY_WORD:
        try:
            return user.parent.childes.get(pk=id)
        except Student.DoesNotExist:
            raise myGraphQLError('Student not found', status=404)

    if user.type == TEACHER_KEY_WORD:
        for teacher_kelaas in user.teacher.kelaases.all():
            if teacher_kelaas.students.filter(pk=id).exists():
                return teacher_kelaas.students.get(pk=id)
        raise myGraphQLError('Student not found', status=404)


def resolve_students(root, info, **kwargs):
    if not info.context.user.is_authenticated:
        raise myGraphQLError('user not authenticated', status=401)
    user = info.context.user.person

    page_size = kwargs.get('page_size', DEFAULT_PAGE_SIZE)
    offset = kwargs.get('page', 1) * page_size

    if user.type == PARENT_KEY_WORD:
        return user.parent.childes.all()[offset - page_size:offset]

    if user.type == TEACHER_KEY_WORD:
        if 'kelaas_id' in kwargs:
            try:
                return Kelaas.objects.get(pk=kwargs['kelaas_id']).students.all()[offset - page_size:offset]
            except Kelaas.DoesNotExist:
                raise myGraphQLError('Kelaas not found', status=404)

    raise myGraphQLError('Permission denied', status=403)


def resolve_kelaas(root, info, id):
    if not info.context.user.is_authenticated:
        raise myGraphQLError('user not authenticated', status=401)
    user = info.context.user.person

    if user.type == TEACHER_KEY_WORD:
        try:
            return user.teacher.kelaases.get(pk=id)
        except Kelaas.DoesNotExist:
            raise myGraphQLError('Kelaas not found', status=404)

    if user.type == PARENT_KEY_WORD:
        for student in user.parent.childes.all():
            if student.kelaases.filter(pk=id).exists():
                return student.kelaases.get(pk=id)
        raise myGraphQLError('Kelaas not found', status=404)

    if user.type == STUDENT_KEY_WORD:
        try:
            return user.student.kelaases.get(pk=id)
        except Kelaas.DoesNotExist:
            raise myGraphQLError('Kelaas not found', status=404)


def resolve_kelaases(root, info, **kwargs):
    if not info.context.user.is_authenticated:
        raise myGraphQLError('user not authenticated', status=401)
    user = info.context.user.person

    page_size = kwargs.get('page_size', DEFAULT_PAGE_SIZE)
    offset = kwargs.get('page', 1) * page_size

    if user.type == TEACHER_KEY_WORD:
        return user.teacher.kelaases.all()[offset - page_size:offset]

    if user.type == PARENT_KEY_WORD:
        try:
            return user.parent.childes.get(pk=kwargs['student_id']).kelaases.all()[offset - page_size:offset]
        except exceptions.KeyError:
            raise myGraphQLError('"student_id" is necessary', status=400)
        except Student.DoesNotExist:
            raise myGraphQLError('Student not found', status=404)

    if user.type == STUDENT_KEY_WORD:
        return user.student.kelaases.all()[offset - page_size:offset]


def resolve_teacher(root, info):
    if not info.context.user.is_authenticated:
        raise myGraphQLError('user not authenticated', status=401)
    user = info.context.user.person

    if user.type == TEACHER_KEY_WORD:
        return user.teacher

    raise myGraphQLError('Permission denied', status=403)


def resolve_parent(root, info):
    if not info.context.user.is_authenticated:
        raise myGraphQLError('user not authenticated', status=401)
    user = info.context.user.person

    if user.type == PARENT_KEY_WORD:
        return user.parent
    raise myGraphQLError('Permission denied', status=403)


def resolve_me(root, info):
    if not info.context.user.is_authenticated:
        raise myGraphQLError('user not authenticated', status=401)
    return info.context.user.person


def resolve_badge_types(root, info, **kwargs):
    if 'id' in kwargs:
        id = kwargs['id']
        return Badge.objects.get(pk=id)

    page_size = kwargs.get('page_size', DEFAULT_PAGE_SIZE)
    offset = kwargs.get('page', 1) * page_size

    return Badge.objects.all()[offset:offset + page_size]


def resolve_certificate(root, info, id):
    try:
        return Certificate.objects.get(pk=id)
    except Certificate.DoesNotExist:
        raise myGraphQLError('Certificate not found', status=404)


def resolve_tags(root, info):
    return Tag.objects.all()


# Query class:
class Query(graphene.ObjectType):
    me = graphene.Field(
        PersonType,
        description="Authetivation required.\n\nreturn basic info about the registered user.",
        resolver=resolve_me,
    )

    student = graphene.Field(
        StudentType,
        description="Authetivation required.\n\nif registered as student, returns current user",
        id=graphene.Int(description="Parent and Teacher: 'id' is necessary. 'id' refers to student_id"),
        resolver=resolve_student,
    )
    students = graphene.List(
        StudentType,
        description="Authetivation required.\n\nParent: return all childrens.\n\n"
                    + "Teacher: a 'kelaas_id' is necessary and return all students on that kelaas,",
        page_size=graphene.Int(),
        page=graphene.Int(),
        kelaas_id=graphene.Int(description="necessary for Teacher"),
        resolver=resolve_students,
    )
    teacher = graphene.Field(
        TeacherType,
        description="Authetivation required.\n\nonly if current user is a teacher.",
        resolver=resolve_teacher
    )
    parent = graphene.Field(
        ParentType,
        description="Authetivation required.\n\nonly if current user is a parent.",
        resolver=resolve_parent
    )

    kelaas = graphene.Field(
        KelaasType,
        description="Authetivation required.\n\n",
        id=graphene.Int(required=True, description="kelaas id."),
        resolver=resolve_kelaas,
    )
    kelaases = graphene.List(
        KelaasType,
        description="Authetivation required.\n\nTeacher: return all teacher's kelaases.\n\n"
                    + "Parent: 'student_id' is necessary and return all of student's kelaases,\n\n"
                    + "(only of parent has access to student)",
        page_size=graphene.Int(),
        page=graphene.Int(),
        student_id=graphene.Int(description="necessary for parents. return all of student's kelaases,"),
        resolver=resolve_kelaases,
    )

    certificate = graphene.Field(
        CertificateType,
        description="Certificate info for certificate page.",
        id=graphene.Int(required=True, description="Certificate id."),
        resolver=resolve_certificate,
    )

    tags = graphene.List(
        TagType,
        description="returns 'all' tags registered in system.",
        resolver=resolve_tags,
    )

    badge_types = graphene.List(
        BadgeModelType,
        description="returns all badges registered in system.\n\n(usage: showing to teacher on assigning page)",
        id=graphene.Int(description="optional, if provided: return badge with related badge_id"),
        page_size=graphene.Int(),
        page=graphene.Int(),
        resolver=resolve_badge_types,
    )
