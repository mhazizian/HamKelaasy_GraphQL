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
        if Add_comment.add_comment(info, data):
            return MessageType(type="success", message="badge_count")

    @staticmethod
    def add_comment(info, data):
        if not info.context.user.is_authenticated:
            raise myGraphQLError('user not authenticated', status=401)
        user = info.context.user.person

        try:
            post = Post.objects.get(pk=data.post_id)
        except Post.DoesNotExist:
            raise myGraphQLError('Post not found', status=404)

        if user.type == STUDENT_KEY_WORD:
            if not user.student.kelaases.filter(pk=post.kelaas_id).exists():
                raise myGraphQLError('Permission denied', status=403)

        if user.type == TEACHER_KEY_WORD:
            if not user.teacher.kelaases.filter(pk=post.kelaas_id).exists():
                raise myGraphQLError('Permission denied', status=403)

        if user.type == PARENT_KEY_WORD:
            access_flag = False
            for student in user.parent.childes.all():
                if student.kelaases.filter(pk=post.kelaas_id).exists():
                    access_flag = True
                    break
            if not access_flag:
                raise myGraphQLError('Permission denied', status=403)

        comment = Comment(
            body=data.body,
            post_id=data.post_id,
            owner_id=user.id,
        )
        comment.save()
        return True
