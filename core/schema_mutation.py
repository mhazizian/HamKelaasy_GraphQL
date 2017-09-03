from graphql import GraphQLError

import graphene
from core.models import *
from graphql_utilz import PersonType, TagType, StudentType, MessageType


class PersonInput(graphene.InputObjectType):
    username = graphene.String(required=True)
    firstName = graphene.String(required=True)


class CreateStudent(graphene.Mutation):
    class Arguments:
        data = PersonInput(required=True)

    Output = MessageType

    def mutate(self, info, data):
        print "Add to db!!"
        return MessageType(type="success", message="User Added to db.")


class Mutation(graphene.ObjectType):
    create_student = CreateStudent.Field()
