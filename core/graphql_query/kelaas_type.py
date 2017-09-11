import graphene
from graphql import GraphQLError

from core.graphql_query.utilz import parent_has_access_to_kelaas, DEFAULT_PAGE_SIZE
from core.models import PARENT_KEY_WORD, STORY_KEY_WORD, KELAAS_POST_KEY_WORD, STUDENT_KEY_WORD


class KelaasType(graphene.ObjectType):
    name = "kelaas"

    id = graphene.Int()
    title = graphene.String()
    shamsi_date = graphene.String()
    description = graphene.String()
    invite_code = graphene.String()

    students = graphene.List(
        'core.graphql_query.StudentType',
        page_size=graphene.Int(),
        page=graphene.Int(),
    )
    kelaas_posts = graphene.List(
        'core.graphql_query.KelaasPostType',
        page_size=graphene.Int(),
        page=graphene.Int(),
    )
    stories = graphene.List(
        'core.graphql_query.StoryType',
        page_size=graphene.Int(),
        page=graphene.Int(),
    )
    tags = graphene.List('core.graphql_query.TagType')

    def resolve_invite_code(self, info):
        user = info.context.user.person

        if self.teachers.filter(pk=user.id).exists():
            return self.invite_code
        if user.type == STUDENT_KEY_WORD:
            if user.student.kelaases.filter(pk=self.id).exists():
                return self.invite_code

        # TODO why pass invite code to parent?!!!!
        if user.type == PARENT_KEY_WORD:
            for student in user.parent.childes.all():
                if student.kelaases.filter(pk=self.id).exists():
                    return self.invite_code

        raise GraphQLError('Permission denied')

    def resolve_tags(self, info):
        return self.tags.all()

    def resolve_students(self, info, **kwargs):
        user = info.context.user.person

        page_size = kwargs.get('page_size', DEFAULT_PAGE_SIZE)
        offset = kwargs.get('page', 1) * page_size

        if self.teachers.filter(pk=user.id).exists():
            return self.students.all()[offset - page_size:offset]
        if user.type == PARENT_KEY_WORD:
            return [student for student in self.students.all() if student.parents.id == user.parent.id][offset - page_size:offset]
        raise GraphQLError('Permission denied')

    def resolve_kelaas_posts(self, info, **kwargs):
        user = info.context.user.person

        page_size = kwargs.get('page_size', DEFAULT_PAGE_SIZE)
        offset = kwargs.get('page', 1) * page_size

        if self.teachers.filter(pk=user.id).exists() or self.students.filter(pk=user.id).exists():
            return self.post_set.filter(type=KELAAS_POST_KEY_WORD).all().reverse()[offset - page_size:offset]

        raise GraphQLError('Permission denied')

    def resolve_stories(self, info, **kwargs):
        user = info.context.user.person

        page_size = kwargs.get('page_size', DEFAULT_PAGE_SIZE)
        offset = kwargs.get('page', 1) * page_size

        if self.teachers.filter(pk=user.id).exists():
            return self.post_set.filter(type=STORY_KEY_WORD).all().reverse()[offset - page_size:offset]

        if user.type == PARENT_KEY_WORD:
            if parent_has_access_to_kelaas(kelaas=self, parent=user.parent):
                return self.post_set.filter(type=STORY_KEY_WORD).all().reverse()[offset - page_size:offset]

        raise GraphQLError('Permission denied')
