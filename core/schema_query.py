from graphql import GraphQLError

import graphene
from core.models import *
from graphql_query import *


def resolve_student(root, info, id, **kwargs):
    if info.context.user.is_authenticated:
        user = info.context.user.person

        if user.type == PARENT_KEY_WORD:
            if user.parent.student_set.filter(pk=id).exists():
                return user.parent.student_set.get(pk=id)
            raise GraphQLError('Student not found')

        if user.type == TEACHER_KEY_WORD:
            for kelaas in user.teacher.kelasses.all():
                if kelaas.students.filter(id=id).exists():
                    return Student.objects.get(pk=id)

    raise GraphQLError('Permission denied')


def resolve_students(root, info, **kwargs):
    if info.context.user.is_authenticated:
        user = info.context.user.person

        if user.type == 'parent':
            return user.parent.student_set.all()

        if user.type == 'teacher':
            if 'kelaas_id' in kwargs:
                if user.teacher.kelasses.filter(id=kwargs['kelaas_id']).exists():
                    return Kelaas.objects.get(pk=kwargs['kelaas_id']).students.all()

    raise GraphQLError('Permission denied')


def resolve_kelaas(root, info, id):
    if info.context.user.is_authenticated:
        user = info.context.user.person

        if user.type == TEACHER_KEY_WORD:
            if user.teacher.kelasses.filter(id=id).exists():
                return user.teacher.kelasses.get(pk=id)
        if user.type == PARENT_KEY_WORD:
            for student in user.parent.student_set.all:
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
            return user.teacher.kelasses.all()
        if user.type == PARENT_KEY_WORD:
            if 'student_id' in kwargs:
                if user.parent.student_set.filter(pl=kwargs['student_id']).exists():
                    return user.parent.student_set.get(pk=kwargs['student_id']).kelaas_set.all()

        if user.type == STUDENT_KEY_WORD:
            return user.student.kelaas_set.all()
    raise GraphQLError('Permission denied')


def resolve_me(root, info):
    if info.context.user.is_authenticated:
        return info.context.user.person
    raise GraphQLError('Permission denied')


def resolve_person(root, info):
    if info.context.user.is_authenticated:
        user = info.context.user.person
        if user.type == STUDENT_KEY_WORD:
            return user.student.parents

    raise GraphQLError('Permission denied')


def resolve_badge_type(root, info):
    return Badge_type.objects.all()


def resolve_persons(root, info):
    return Person.objects.all()


def resolve_tags(root, info):
    return Tag.objects.all()


# Query class:
class Query(graphene.ObjectType):
    me = graphene.Field(
        PersonType,
        resolver=resolve_me,
    )

    # for test:
    persons = graphene.List(
        PersonType,
        resolver=resolve_persons,
    )

    student = graphene.Field(
        StudentType,
        id=graphene.Int(required=True),
        kelaas_id=graphene.Int(),
        resolver=resolve_student,
    )
    students = graphene.List(
        StudentType,
        kelaas_id=graphene.Int(),
        resolver=resolve_students,
    )

    kelaas = graphene.Field(
        KelaasType,
        id=graphene.Int(required=True),
        resolver=resolve_kelaas,
    )
    kelaases = graphene.List(
        KelaasType,
        student_id=graphene.Int(),
        resolver=resolve_kelaases,
    )
    parent = graphene.Field(
        PersonType,
        resolver=resolve_parent,
    )

    badge_type = graphene.List(
        BadgeModelType,
        id=graphene.Int(),
        resolver=resolve_badge_type,
    )

    tags = graphene.List(
        TagType,
        resolver=resolve_tags,
    )
