import graphene

from core.graphql_query import DEFAULT_PAGE_SIZE


class PostType(graphene.ObjectType):
    name = "post"

    id = graphene.Int()
    title = graphene.String()
    description = graphene.String()
    shamsi_date = graphene.String()
    time_passed = graphene.String()
    type = graphene.String()

    comments = graphene.List(
        'core.graphql_query.CommentType',
        page_size=graphene.Int(),
        page=graphene.Int(),
    )

    def resolve_comments(self, info, **kwargs):
        page_size = kwargs.get('page_size', DEFAULT_PAGE_SIZE)
        offset = kwargs.get('page', 1) * page_size

        if page_size == offset:
            return self.comments.all()[-offset:][::-1]
        return self.comments.all()[-offset:-offset + page_size][::-1]