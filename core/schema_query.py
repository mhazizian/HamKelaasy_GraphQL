from graphql import GraphQLError

import graphene
from core.models import *
from graphql_utilz import PersonType, TagType, StudentType


def resolve_student(root, info, **kwargs):
    if info.context.user.is_authenticated:
        user = info.context.user.person

        if user.type is 'parent':
            if user.parent.student_set.filter(pk=kwargs['id']).exists():
                return user.parent.student_set.get(pk=kwargs['id'])
            raise GraphQLError('Student not found')

        if user.type is 'teacher':
            # permission check
            return Student.objects.get(pk=kwargs['id'])
    # for test:
    # raise GraphQLError('Permission denied')
    return Student.objects.get(pk=kwargs['id'])


def resolve_students(root, info, **kwargs):
    if info.context.user.is_authenticated:
        user = info.context.user.person

        if user.type is 'parent':
            return user.parent.student_set.all()

        if user.type is 'teacher':
            if 'kelaas_id' in kwargs:
                if user.teacher.kelasses.filter(id=kwargs['kelaas_id']).exists():
                    return Kelaas.objects.get(pk=kwargs['kelaas_id']).students.all()

    # raise GraphQLError('Permission denied')
    # for test:
    return Student.objects.all()


def resolve_persons(root, info):
    return Person.objects.all()


def resolve_tags(root, info):
    return Tag.objects.all()


# Query class:
class Query(graphene.ObjectType):
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
    tags = graphene.List(
        TagType,
        resolver=resolve_tags,
    )
