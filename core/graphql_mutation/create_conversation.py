import graphene

from core import myGraphQLError

from core.graphql_query import ConversationType
from core.models import Conversation, Person, Kelaas


class Create_convesation_input(graphene.InputObjectType):
    members_id = graphene.String(required=True, description="a string of member id.\n\nexample: '1,2,10,4'\n\n"
                                                            "by default: current user is joined this conversation ")
    kelaas_id = graphene.Int(requierd=True)


class Create_convesation(graphene.Mutation):
    class Arguments:
        data = Create_convesation_input(required=True)

    Output = ConversationType

    def mutate(self, info, data):
        return Create_convesation.create(info, data)

    @staticmethod
    def create(info, data):
        # TODO permission denied!!

        if not info.context.user.is_authenticated:
            raise myGraphQLError('user not authenticated', status=401)
        user = info.context.user.person

        try:
            kelaas = Kelaas.objects.get(pk=data.kelaas_id)
            members_id = [int(id) for id in data.members_id.split(',')]
            members_id.append(user.id)
            members = Person.objects.filter(id__in=members_id)

            for conv in kelaas.conversations.all():
                if conv.member_count == len(members):
                    if conv.members.filter(id__in=[member.id for member in members]):
                        return conv

            convesation = Conversation(kelaas_id=kelaas.id)
            convesation.save()

            for person in members:
                convesation.members.add(person)
            convesation.save()
            return convesation

        except Person.DoesNotExist:
            raise myGraphQLError('Person not found', status=404)
        except Kelaas.DoesNotExist:
            raise myGraphQLError('Kelaas not found', status=404)
