import graphene
import core.services as services
from core import myGraphQLError


class Delete_comment_input(graphene.InputObjectType):
    comment_id = graphene.Int(required=True)


class Delete_comment(graphene.Mutation):
    class Arguments:
        data = Delete_comment_input(required=True)

    def mutate(self, info, data):
        return Delete_comment.delete(info, data)

    @staticmethod
    def delete(info, data):
        if not info.context.user.is_authenticated:
            raise myGraphQLError('user not authenticated', status=401)
        user = info.context.user.person

        return services.delete_comment(
            user=user,
            comment_id=data.comment_id,
        )
