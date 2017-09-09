import graphene
from core.graphql_query import MessageType
from core.models import TEACHER_KEY_WORD, Student, Badge_link, Badge


class Assign_badge_input(graphene.InputObjectType):
    kelaas_id = graphene.Int(required=True)
    badges = graphene.String(required=True, description="a string of badge_id.\n\nexample: '1,2,10,4'")
    student_id = graphene.Int(required=True)


class Assign_badge(graphene.Mutation):
    class Arguments:
        data = Assign_badge_input(required=True)

    Output = MessageType

    def mutate(self, info, data):
        if info.context.user.is_authenticated:
            if Assign_badge.assign_badge(info, data):
                return MessageType(type="success", message="badge_count")

        return MessageType(type="error", message="Permission denied.")

    @staticmethod
    def assign_badge(info, data):
        user = info.context.user.person
        if not user.type == TEACHER_KEY_WORD:
            return False
        teacher = user.teacher

        if not teacher.kelaases.filter(pk=data.kelaas_id).exists():
            return False
        kelaas = user.teacher.kelaases.get(pk=data.kelaas_id)

        if not Student.objects.filter(pk=data.student_id).exists():
            return False
        student = Student.objects.get(pk=data.student_id)

        if not student.kelaases.filter(pk=kelaas.id).exists():
            return False

        for badge_id in data.badges.split(','):
            if Badge_link.objects.filter(student=student, type_id=badge_id, kelaas=kelaas).exists():
                t = Badge_link.objects.filter(student=student, type_id=badge_id, kelaas=kelaas).first()
                t.count = t.count + 1
                t.save()
            else:
                if Badge.objects.filter(pk=badge_id).exists():
                    t = Badge_link(
                        student=student,
                        kelaas=kelaas,
                        type_id=badge_id,
                    )
                    t.save()
        return True