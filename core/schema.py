from core.models import *

# from graphene import ObjectType, Node, Schema
# from graphene_django.fields import DjangoConnectionField
#
# from graphene_django.types import DjangoObjectType
# from graphene import relay

import graphene
from graphql_utilz import PersonType, TagType, StudentType, UserType


class Query(graphene.ObjectType):
    person = graphene.Field(
        PersonType,
        id=graphene.Int()
    )
    all_persons = graphene.List(PersonType)

    student = graphene.Field(
        StudentType,
        id=graphene.Int()
    )
    students = graphene.List(
        StudentType,
        parent_id=graphene.Int(),
        kelaas_id=graphene.Int()
    )
    all_tags = graphene.List(TagType)

    user_type = graphene.String()

    def resolve_all_person(self, info):
        return Person.objects.all()

    def resolve_person(self, info):
        # if 'id' in args:
        #     return Person.objects.get(pk=args.get('id'))
        return Person.objects.get(pk=2)

    def resolve_all_tags(self, info):
        return Tag.objects.all()

    def resolve_student(self, info, **args):
            return Student.objects.get(pk=args['id'])

    def resolve_students(self, args, context, info):
        if 'parent_id' in args:
            return Parent.objects.get(pk=args.get('parent_id')).student_set.all()
        if 'kelaas_id' in args:
            return Kelaas.objects.get(pk=args.get('kelaas_id')).students.all()

    def resolve_user_type(self, info):
        return "hi"
        # if context.user.is_authenticated():
        #     return context.user.username
        # return "False"


schema = graphene.Schema(query=Query)
