import graphene
from core import myGraphQLError

from core.graphql_query import MessageType
from core.models import TEACHER_KEY_WORD, Student, Badge_link, Badge, Kelaas


class Assign_badge_input(graphene.InputObjectType):
    kelaas_id = graphene.Int(required=True)
    badges = graphene.String(required=True, description="a string of badge_id.\n\nexample: '1,2,10,4'")
    student_id = graphene.Int(required=True)


class Assign_badge(graphene.Mutation):
    class Arguments:
        data = Assign_badge_input(required=True)

    Output = MessageType

    def mutate(self, info, data):
        if Assign_badge.assign_badge(info, data):
            return MessageType(type="success", message="badge_count")

    @staticmethod
    def assign_badge(info, data):
        if not info.context.user.is_authenticated:
            raise myGraphQLError('user not authenticated', status=401)
        user = info.context.user.person

        if not user.type == TEACHER_KEY_WORD:
            raise myGraphQLError('Permission denied', status=403)
        teacher = user.teacher

        if not teacher.kelaases.filter(pk=data.kelaas_id).exists():
            return False
        try:
            kelaas = user.teacher.kelaases.get(pk=data.kelaas_id)
            student = Student.objects.get(pk=data.student_id)
        except Kelaas.DoesNotExist:
            raise myGraphQLError('Kelaas not found', status=404)
        except Student.DoesNotExist:
            raise myGraphQLError('Student not found', status=404)

        for badge_id in data.badges.split(','):
            if Badge_link.objects.filter(student=student, type_id=badge_id, kelaas=kelaas).exists():
                t = Badge_link.objects.filter(student=student, type_id=badge_id, kelaas=kelaas).first()
                t.count = t.count + 1
                t.save()
            else:
                if not Badge.objects.filter(pk=badge_id).exists():
                    raise myGraphQLError('Badge not found', status=404)
                t = Badge_link(
                    student=student,
                    kelaas=kelaas,
                    type_id=badge_id,
                )
                t.save()
        return True
