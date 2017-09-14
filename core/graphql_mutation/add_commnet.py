import graphene
from core import myGraphQLError

from core.graphql_query import MessageType
from core.models import TEACHER_KEY_WORD, Post, STUDENT_KEY_WORD, PARENT_KEY_WORD, Comment


class Add_comment_input(graphene.InputObjectType):
    body = graphene.String(required=True)
    post_id = graphene.Int(required=True)


class Add_comment(graphene.Mutation):
    class Arguments:
        data = Add_comment_input(required=True)

    Output = MessageType

    def mutate(self, info, data):
        if info.context.user.is_authenticated:
            if Add_comment.add_comment(info, data):
                return MessageType(type="success", message="badge_count")
            raise myGraphQLError('Bad data input')

        raise myGraphQLError('Permission denied')

    @staticmethod
    def add_comment(info, data):
        user = info.context.user.person
        if not Post.objects.filter(pk=data.post_id).exists():
            return False
        post = Post.objects.get(pk=data.post_id)

        if user.type == STUDENT_KEY_WORD:
            if not user.student.kelaases.filter(pk=post.kelaas_id).exists():
                return False

        if user.type == TEACHER_KEY_WORD:
            if not user.teacher.kelaases.filter(pk=post.kelaas_id).exists():
                return False

        if user.type == PARENT_KEY_WORD:
            f = False
            for student in user.parent.childes.all():
                if student.kelaases.filter(pk=post.kelaas_id).exists():
                    f = True
                    break
            if not f:
                return False

        comment = Comment(
            body=data.body,
            post_id=data.post_id,
            owner_id=user.id,
        )
        comment.save()
        return True
