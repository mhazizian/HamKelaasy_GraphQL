import graphene
from core import services


class KelaasType(graphene.ObjectType):
    name = "kelaas"

    id = graphene.Int()
    title = graphene.String()
    shamsi_date = graphene.String()
    description = graphene.String()
    invite_code = graphene.String()
    gender = graphene.Int(description='1 for men, 0 for women, 2 for both!')
    teacher = graphene.Field('core.graphql_query.TeacherType')

    conversations = graphene.List(
        'core.graphql_query.ConversationType',
        page_size=graphene.Int(default_value=services.DEFAULT_PAGE_SIZE),
        page=graphene.Int(default_value=1),
    )
    conversation = graphene.Field(
        'core.graphql_query.ConversationType',
        id=graphene.Int(required=True)
    )

    students = graphene.List(
        'core.graphql_query.StudentType',
        page_size=graphene.Int(default_value=services.DEFAULT_PAGE_SIZE),
        page=graphene.Int(default_value=1),
    )
    kelaas_posts = graphene.List(
        'core.graphql_query.KelaasPostType',
        page_size=graphene.Int(default_value=services.DEFAULT_PAGE_SIZE),
        page=graphene.Int(default_value=1),
    )
    stories = graphene.List(
        'core.graphql_query.StoryType',
        page_size=graphene.Int(default_value=services.DEFAULT_PAGE_SIZE),
        page=graphene.Int(default_value=1),
    )
    tags = graphene.List('core.graphql_query.TagType')

    def resolve_invite_code(self, info):
        user = info.context.user.person
        return services.kelaas__get_invite_code(kelaas=self, user=user)

    def resolve_tags(self, info):
        return services.kelaas__get_tags(self)

    def resolve_students(self, info, page, page_size):
        user = info.context.user.person

        query_set = services.kelaas__get_student(kelaas=self, user=user)
        return services.apply_pagination(query_set, page_size=page_size, page=page)

    def resolve_kelaas_posts(self, info, page, page_size):
        user = info.context.user.person

        query_set = services.kelaas__get_kelaas_post(kelaas=self, user=user)
        return services.apply_pagination(query_set, page=page, page_size=page_size)

    def resolve_stories(self, info, page, page_size):
        user = info.context.user.person

        query_set = services.kelaas_get_stories(kelaas=self, user=user)
        return services.apply_pagination(query_set, page=page, page_size=page_size)

    def resolve_conversations(self, info, page, page_size):
        user = info.context.user.person

        query_set = services.kelaas__get_conversations(kelaas=self, user=user)
        return services.apply_pagination(query_set, page=page, page_size=page_size)

    def resolve_conversation(self, info, id):
        user = info.context.user.person
        return services.kelaas__get_conversation(kelaas=self, user=user, conversation_id=id)
