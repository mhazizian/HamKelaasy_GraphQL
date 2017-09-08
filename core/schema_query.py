from graphql import GraphQLError

import graphene
from core.models import *
from graphql_query import *


def resolve_student(root, info, **kwargs):
    if info.context.user.is_authenticated:
        user = info.context.user.person
        if user.type == STUDENT_KEY_WORD:
            return user.student

        id = kwargs['id']
        if user.type == PARENT_KEY_WORD:
            if user.parent.student_set.filter(pk=id).exists():
                return user.parent.student_set.get(pk=id)
            raise GraphQLError('Student not found')

        if user.type == TEACHER_KEY_WORD:
            for kelaas in user.teacher.kelaases.all():
                if kelaas.students.filter(id=id).exists():
                    return Student.objects.get(pk=id)

    raise GraphQLError('Permission denied')


def resolve_students(root, info, **kwargs):
    if info.context.user.is_authenticated:
        user = info.context.user.person

        if user.type == PARENT_KEY_WORD:
            return user.parent.student_set.all()

        if user.type == TEACHER_KEY_WORD:
            if 'kelaas_id' in kwargs:
                if user.teacher.kelaases.filter(id=kwargs['kelaas_id']).exists():
                    return Kelaas.objects.get(pk=kwargs['kelaas_id']).students.all()

    raise GraphQLError('Permission denied')


def resolve_kelaas(root, info, id):
    if info.context.user.is_authenticated:
        user = info.context.user.person

        if user.type == TEACHER_KEY_WORD:
            if user.teacher.kelaases.filter(id=id).exists():
                return user.teacher.kelaases.get(pk=id)
        if user.type == PARENT_KEY_WORD:
            for student in user.parent.student_set.all():
                if student.kelaas_set.filter(pk=id).exists():
                    return student.kelaas_set.get(pk=id)
        if user.type == STUDENT_KEY_WORD:
            if user.student.kelaas_set.filter(pk=id).exists():
                return user.student.kelaas_set.get(pk=id)
    raise GraphQLError('Permission denied')


def resolve_kelaases(root, info, **kwargs):
    if info.context.user.is_authenticated:
        user = info.context.user.person

        if user.type == TEACHER_KEY_WORD:
            return user.teacher.kelaases.all()
        if user.type == PARENT_KEY_WORD:
            if 'student_id' in kwargs:
                if user.parent.student_set.filter(pl=kwargs['student_id']).exists():
                    return user.parent.student_set.get(pk=kwargs['student_id']).kelaas_set.all()

        if user.type == STUDENT_KEY_WORD:
            return user.student.kelaas_set.all()
    raise GraphQLError('Permission denied')


def resolve_teacher(root, info):
    if info.context.user.is_authenticated:
        user = info.context.user.person

        if user.type == TEACHER_KEY_WORD:
            return user.teacher
    raise GraphQLError('Permission denied')


def resolve_parent(root, info):
    if info.context.user.is_authenticated:
        user = info.context.user.person

        if user.type == PARENT_KEY_WORD:
            return user.parent
    raise GraphQLError('Permission denied')


def resolve_me(root, info):
    if info.context.user.is_authenticated:
        return info.context.user.person
    raise GraphQLError('Permission denied')


def resolve_badge_type(root, info, **kwargs):
    if 'id' in kwargs:
        id = kwargs['id']
        return Badge.objects.get(pk=id)
    return Badge.objects.all()


def resolve_certificate(root, info, id):
    if Certificate.objects.filter(pk=id).exists():
        return Certificate.objects.get(pk=id)


# def resolve_persons(root, info):
#     return Person.objects.all()


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
        description="returns all tags registered in system.",
        resolver=resolve_tags,
    )

    badge_types = graphene.List(
        BadgeModelType,
        description="returns all badges registered in system.\n\n(usage: showing to teacher on assigning page)",
        id=graphene.Int(description="optional, if provided: return badge with related badge_id"),
        resolver=resolve_badge_type,
    )
