import graphene
from core.models import STUDENT_KEY_WORD, TEACHER_KEY_WORD, PARENT_KEY_WORD


class KelaasType(graphene.ObjectType):
    name = "kelaas"

    id = graphene.Int()
    title = graphene.String()
    shamsi_date = graphene.String()
    description = graphene.String()
    invite_code = graphene.String()

    students = graphene.List('core.graphql_utilz.StudentType')
    kelaas_post = graphene.List('core.graphql_utilz.KelaasPostType')
    story = graphene.List('core.graphql_utilz.StoryType')
    tags = graphene.List('core.graphql_utilz.TagType')

    def resolve_tags(self, info):
        return self.tags.all()

    def resolve_students(self, info):
        user = info.context.user.person

        if user.type == "teacher":
            return self.students.all()
        if user.type == "parent":
            return [student for student in self.students.all() if student.parents.id == user.parent.id]

    def resolve_kelaas_post(kelaas, info):
        user = info.context.user.person

        if user.type == STUDENT_KEY_WORD or user.type == TEACHER_KEY_WORD:
            return kelaas.kelaas_post_set.all()

    def resolve_story(kelaas, info):
        user = info.context.user.person

        if user.type == TEACHER_KEY_WORD or user.type == PARENT_KEY_WORD:
            return kelaas.story_set.all()
