import graphene
from core import myGraphQLError

from core.graphql_query.utilz import parent_has_access_to_kelaas, DEFAULT_PAGE_SIZE, teacher_has_access_to_kelaas
from core.models import PARENT_KEY_WORD, STORY_KEY_WORD, KELAAS_POST_KEY_WORD, STUDENT_KEY_WORD, TEACHER_KEY_WORD


class KelaasType(graphene.ObjectType):
    name = "kelaas"

    id = graphene.Int()
    title = graphene.String()
    shamsi_date = graphene.String()
    description = graphene.String()
    invite_code = graphene.String()

    conversations = graphene.List(
        'core.graphql_query.ConversationType',
        page_size=graphene.Int(),
        page=graphene.Int(),
    )

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

        if user.type == TEACHER_KEY_WORD:
            if teacher_has_access_to_kelaas(self, user.teacher):
                return self.invite_code
            raise myGraphQLError('Permission denied', status=403)

        if user.type == STUDENT_KEY_WORD:
            if user.student.kelaases.filter(pk=self.id).exists():
                return self.invite_code
            raise myGraphQLError('Permission denied', status=403)

        # TODO why pass invite code to parent?!!!!
        if user.type == PARENT_KEY_WORD:
            for student in user.parent.childes.all():
                if student.kelaases.filter(pk=self.id).exists():
                    return self.invite_code
            raise myGraphQLError('Permission denied', status=403)

    def resolve_tags(self, info):
        return self.tags.all()

    def resolve_students(self, info, **kwargs):
        user = info.context.user.person

        page_size = kwargs.get('page_size', DEFAULT_PAGE_SIZE)
        offset = kwargs.get('page', 1) * page_size

        if user.type == TEACHER_KEY_WORD:
            if teacher_has_access_to_kelaas(self, user.teacher):
                return self.students.all()[offset - page_size:offset]
            raise myGraphQLError('Permission denied', status=403)

        if user.type == PARENT_KEY_WORD:
            return [student for student in self.students.all() if student.parents.id == user.parent.id][
                   offset - page_size:offset]

        raise myGraphQLError('Permission denied', status=403)

    def resolve_kelaas_posts(self, info, **kwargs):
        user = info.context.user.person

        page_size = kwargs.get('page_size', DEFAULT_PAGE_SIZE)
        offset = kwargs.get('page', 1) * page_size

        if teacher_has_access_to_kelaas(self, user.teacher) or self.students.filter(pk=user.id).exists():
            print "here"
            return self.post_set.filter(type=KELAAS_POST_KEY_WORD).order_by('-id')[offset - page_size:offset]

        raise myGraphQLError('Permission denied', status=403)

    def resolve_stories(self, info, **kwargs):
        user = info.context.user.person

        page_size = kwargs.get('page_size', DEFAULT_PAGE_SIZE)
        offset = kwargs.get('page', 1) * page_size

        if user.type == TEACHER_KEY_WORD:
            if teacher_has_access_to_kelaas(self, user.teacher):
                return self.post_set.filter(type=STORY_KEY_WORD).all().order_by('-id')[offset - page_size:offset]

        if user.type == PARENT_KEY_WORD:
            if parent_has_access_to_kelaas(kelaas=self, parent=user.parent):
                return self.post_set.filter(type=STORY_KEY_WORD).all().order_by('-id')[offset - page_size:offset]

        raise myGraphQLError('Permission denied', status=403)

    def resolve_conversations(self, info, **kwargs):
        user = info.context.user.person

        page_size = kwargs.get('page_size', DEFAULT_PAGE_SIZE)
        offset = kwargs.get('page', 1) * page_size

        return self.conversations.filter(members__id=user.id).order_by('-last_message_time')[offset - page_size:offset]

