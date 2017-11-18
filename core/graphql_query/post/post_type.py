import graphene
import core.services as services


class PostType(graphene.ObjectType):
    name = "post"

    id = graphene.Int()
    title = graphene.String()
    description = graphene.String()
    shamsi_date = graphene.String()
    time_passed = graphene.String()
    type = graphene.String()
    owner = graphene.Field('core.graphql_query.PersonType')
    seen_count = graphene.Int()
    i_have_seen = graphene.Boolean()

    comments = graphene.List(
        'core.graphql_query.CommentType',
        page_size=graphene.Int(default_value=services.DEFAULT_PAGE_SIZE),
        page=graphene.Int(default_value=1),
    )
    comment_count = graphene.Int()

    def resolve_comments(self, info, page, page_size):
        user = info.context.user.person

        query_set = services.post__get_comments(post=self, user=user)
        return services.apply_pagination(query_set, page=page, page_size=page_size)

    def resolve_comment_count(self, info):
        user = info.context.user.person
        return services.post__get_comments_count(post=self, user=user)

    def resolve_owner(self, info):
        return self.owner

    def resolve_seen_count(self, info):
        user = info.context.user.person
        return services.get_post_seen_count(user=user, post=self)

    def resolve_i_have_seen(self, info):
        user = info.context.user.person
        return services.user_has_seen_post(user=user, post=self)