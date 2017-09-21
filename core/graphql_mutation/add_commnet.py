import graphene
import core.services as services
from core import myGraphQLError

from core.graphql_query import CommentType


class Add_comment_input(graphene.InputObjectType):
    body = graphene.String(required=True)
    post_id = graphene.Int(required=True)


class Add_comment(graphene.Mutation):
    class Arguments:
        data = Add_comment_input(required=True)

    Output = CommentType

    def mutate(self, info, data):
        return Add_comment.add_comment(info, data)

    @staticmethod
    def add_comment(info, data):
        if not info.context.user.is_authenticated:
            raise myGraphQLError('user not authenticated', status=401)
        user = info.context.user.person

        return services.add_comment(
            user=user,
            post_id=data.post_id,
            body=data.body,
        )
