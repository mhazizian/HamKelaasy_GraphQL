import graphene
from graphql import GraphQLError

from core.graphql_utilz.utilz import it_is_him, parent_has_access_to_kelaas
from core.models import STUDENT_KEY_WORD, TEACHER_KEY_WORD, PARENT_KEY_WORD, STORY_KEY_WORD, KELAAS_POST_KEY_WORD


class KelaasType(graphene.ObjectType):
    name = "kelaas"

    id = graphene.Int()
    title = graphene.String()
    shamsi_date = graphene.String()
    description = graphene.String()
    invite_code = graphene.String()

    students = graphene.List('core.graphql_utilz.StudentType')
    kelaas_posts = graphene.List('core.graphql_utilz.KelaasPostType')
    stories = graphene.List('core.graphql_utilz.StoryType')
    tags = graphene.List('core.graphql_utilz.TagType')

    def resolve_invite_code(self, info):
        user = info.context.user.person

        if self.teacher_set.filter(pk=user.id).exists():
            return self.invite_code
        raise GraphQLError('Permission denied')

    def resolve_tags(self, info):
        return self.tags.all()

    def resolve_students(self, info):
        user = info.context.user.person

        if self.teacher_set.filter(pk=user.id).exists():
            return self.students.all()
        if user.type == PARENT_KEY_WORD:
            return [student for student in self.students.all() if student.parents.id == user.parent.id]
        raise GraphQLError('Permission denied')

    def resolve_kelaas_posts(self, info):
        user = info.context.user.person

        if self.teacher_set.filter(pk=user.id).exists() or self.students.filter(pk=user.id).exists():
            return self.post_set.filter(type=KELAAS_POST_KEY_WORD).all()

        raise GraphQLError('Permission denied')

    def resolve_stories(self, info):
        user = info.context.user.person

        if self.teacher_set.filter(pk=user.id).exists():
            return self.post_set.filter(type=STORY_KEY_WORD).all()

        if user.type == PARENT_KEY_WORD:
            if parent_has_access_to_kelaas(kelaas=self, parent=user.parent):
                return self.post_set.filter(type=STORY_KEY_WORD).all()

        raise GraphQLError('Permission denied')
