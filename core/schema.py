from graphql import GraphQLError

from core.models import *

# from graphene import ObjectType, Node, Schema
# from graphene_django.fields import DjangoConnectionField
#
# from graphene_django.types import DjangoObjectType
# from graphene import relay

import graphene
from graphql_utilz import PersonType, TagType, StudentType, UserType


class Query(graphene.ObjectType):
    persons = graphene.List(
        PersonType,
    )

    student = graphene.Field(
        StudentType,
        id=graphene.Int(required=True),
        kelaas_id=graphene.Int()
    )
    students = graphene.List(
        StudentType,
        kelaas_id=graphene.Int()
    )
    tags = graphene.List(TagType)

    # user_type = graphene.String()





    def resolve_student(self, info, **kwargs):
        if info.context.user.is_authenticated:
            user = info.context.user.person

            if user.type is 'parent':
                if user.parent.student_set.filter(pk=kwargs['id']).exists():
                    return user.parent.student_set.get(pk=kwargs['id'])
                raise GraphQLError('Student not found')

            if user.type is 'teacher':
                # permission check
                return Student.objects.get(pk=kwargs['id'])

        # raise GraphQLError('Permission denied')
        # for test:
        return Student.objects.get(pk=kwargs['id'])

    def resolve_students(self, info, **kwargs):
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



    # for test:
    def resolve_persons(self, info):
        return Person.objects.all()

    def resolve_tags(self, info):
        return Tag.objects.all()


        # def resolve_students(self, args, context, info):
        #     if 'parent_id' in args:
        #         return Parent.objects.get(pk=args.get('parent_id')).student_set.all()
        #     if 'kelaas_id' in args:
        #         return Kelaas.objects.get(pk=args.get('kelaas_id')).students.all()
        #
        # def resolve_user_type(self, info):
        #     return "hi"
        #     # if context.user.is_authenticated():
        #     #     return context.user.username
        #     # return "False"


schema = graphene.Schema(query=Query)
