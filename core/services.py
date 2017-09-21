from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from core import myGraphQLError
from core.models import Parent, TEACHER_KEY_WORD, PARENT_KEY_WORD, Kelaas, KELAAS_POST_KEY_WORD, STORY_KEY_WORD, \
    STUDENT_KEY_WORD, Post, Person, Student, Tag, Comment, Badge_link, Badge, File, Kelaas_post, Story, Conversation, \
    Conversation_message

DEFAULT_PAGE_SIZE = 10


def apply_pagination(input_list, page=1, page_size=DEFAULT_PAGE_SIZE):
    paginator = Paginator(input_list, page_size)

    try:
        res = paginator.page(page)
    except PageNotAnInteger:
        res = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        res = paginator.page(paginator.num_pages)

    return res


def parent_has_access_to_kelaas(kelaas, parent):
    for student in parent.childes.all():
        if kelaas.students.filter(pk=student.id).exists():
            return True
    return False


def teacher_has_access_to_kelaas(kelaas, teacher):
    if kelaas.teachers.filter(pk=teacher.id).exists():
        return True
    return False


# ______________________________________________________________________________________________________
# ______________________________________________________________________________________________________



def parent__get_childes(parent, user, **kwargs):
    # type: (Parent, Person) -> object
    if parent.id == user.id:
        return parent.childes.all()

    if user.type == TEACHER_KEY_WORD:
        if 'kelaas_id' in kwargs:
            if user.kelaases.filter(kelaas_id=kwargs['kelaas_id']).exist():
                return parent.childes.filter(kelaases__in=[kwargs['kelaas_id']])
            raise myGraphQLError('Permission denied', status=403)

        result = []
        # user.kelaases.filter(students__in=[child.id for child in parent.childes.all()])
        for child in parent.childes.all():
            if child.kelaases.filter(teachers__in=[user.id]).exists():
                result.append(child)
        return result

    raise myGraphQLError('Permission denied', status=403)


def parent__get_child(parent, user, childe_id):
    try:
        if parent.id == user.id:
            return parent.childes.get(pk=childe_id)

        if user.type == TEACHER_KEY_WORD:
            child = parent.childes.get(pk=childe_id)
            if child.kelaases.filter(teachers__in=[user.id]).exists():
                return child

    except Student.DoesNotExist:
        raise myGraphQLError('Child not found', status=404)

    raise myGraphQLError('Permission denied', status=403)


def teacher__get_kelaases(teacher, user):
    if not user.id == teacher.id:
        raise myGraphQLError('Permission denied', status=403)

    return teacher.kelaases.all().order_by('-id')


def teacher__get_kelaas(teacher, user, kelaas_id):
    if not user.id == teacher.id:
        raise myGraphQLError('Permission denied', status=403)

    try:
        return teacher.kelaases.get(pk=kelaas_id)
    except Kelaas.DoesNotExist:
        raise myGraphQLError('Kelaas not found', status=404)


def student__get_invite_code(student, user):
    if student.id == user.id:
        return student.parent_code
    raise myGraphQLError('Permission denied', status=403)


def student__get_kelaases(student, user):
    if user.id == student.id:
        return student.kelaases.all().order_by('-id')

    if user.type == TEACHER_KEY_WORD:
        return [kelaas for kelaas in student.kelaases.all() if
                user.teacher.kelaases.filter(id=kelaas.id).exists()].reverse()

    if user.type == PARENT_KEY_WORD and user.id == student.parents.id:
        return student.kelaases.all().order_by('-id')

    raise myGraphQLError('Permission denied', status=403)


def student__get_kelaas(student, user, kelaas_id):
    try:
        if user.id == student.id:
            return student.kelaases.get(pk=kelaas_id)

        if user.type == PARENT_KEY_WORD and user.id == student.parents.id:
            return student.kelaases.get(pk=kelaas_id)

        if user.type == TEACHER_KEY_WORD:
            if user.teacher.kelaases.filter(pk=kelaas_id).exists():
                return student.kelaases.get(pk=kelaas_id)
    except Kelaas.DoesNotExist:
        raise myGraphQLError('Kelaas not found', status=404)

    raise myGraphQLError('Permission denied', status=403)


def student__get_badges(student, user, **kwargs):
    if user.id == student.id:
        if 'kelaas_id' in kwargs:
            return student.badges.filter(kelaas_id=kwargs['kelaas_id'])
        return student.badges.all()

    if user.type == TEACHER_KEY_WORD:
        if 'kelaas_id' in kwargs:
            if user.teacher.kelaases.filter(id=kwargs['kelaas_id']).exists():
                return student.badges.filter(kelaas_id=kwargs['kelaas_id'])

        badges = []
        for kelaas in user.teacher.kelaases.all():
            if kelaas.students.filter(pk=student.id).exists():
                badges.extend(student.badges.filter(kelaas=kelaas))
        return badges

    if user.type == PARENT_KEY_WORD and user.id == student.parents.id:
        if 'kelaas_id' in kwargs:
            student.badges.filter(kelaas_id=kwargs['kelaas_id'])
        return student.badges.all()

    raise myGraphQLError('Permission denied', status=403)


def student__get_parent(student, user):
    if user.id == student.id:
        return student.parents

    if user.type == TEACHER_KEY_WORD:
        for kelaas in user.teacher.kelaases.all():
            if kelaas.students.filter(pk=student.id).exists():
                return student.parents

    if user.type == PARENT_KEY_WORD and user.id == student.parents.id:
        return student.parents

    raise myGraphQLError('Permission denied', status=403)


def kelaas__get_tags(kelaas):
    return kelaas.tags.all()


def kelaas__get_student(kelaas, user):
    if user.type == TEACHER_KEY_WORD:
        if teacher_has_access_to_kelaas(kelaas=kelaas, teacher=user.teacher):
            return kelaas.students.all()

    if user.type == PARENT_KEY_WORD:
        return kelaas.students.filter(parents_id=user.id)

    raise myGraphQLError('Permission denied', status=403)


def kelaas__get_kelaas_post(kelaas, user):
    if teacher_has_access_to_kelaas(kelaas, user.teacher) or kelaas.students.filter(pk=user.id).exists():
        return kelaas.posts.filter(type=KELAAS_POST_KEY_WORD).order_by('-id')

    raise myGraphQLError('Permission denied', status=403)


def kelaas_get_stories(kelaas, user):
    if user.type == TEACHER_KEY_WORD:
        if teacher_has_access_to_kelaas(kelaas, user.teacher):
            return kelaas.posts.filter(type=STORY_KEY_WORD).all().order_by('-id')

    if user.type == PARENT_KEY_WORD:
        if parent_has_access_to_kelaas(kelaas=kelaas, parent=user.parent):
            return kelaas.posts.filter(type=STORY_KEY_WORD).all().order_by('-id')

    raise myGraphQLError('Permission denied', status=403)


def kelaas__get_conversations(kelaas, user):
    return kelaas.conversations.filter(members__id=user.id).order_by('-last_message_time')


def kelaas__get_conversation(kelaas, user, conversation_id):
    # TODO exception handling(in case of invalid id)
    return kelaas.conversations.filter(members__id=user.id, id=conversation_id).first()


def kelaas__get_invite_code(kelaas, user):
    # type: (Kelaas, Person) -> string
    if user.type == TEACHER_KEY_WORD:
        if teacher_has_access_to_kelaas(kelaas, user.teacher):
            return kelaas.invite_code

    if user.type == STUDENT_KEY_WORD:
        if user.student.kelaases.filter(pk=kelaas.id).exists():
            return kelaas.invite_code

    # TODO why pass invite code to parent?!!!!
    if user.type == PARENT_KEY_WORD:
        if parent_has_access_to_kelaas(kelaas=kelaas, parent=user.parent):
            return kelaas.invite_code

    raise myGraphQLError('Permission denied', status=403)


def post__get_comments(post, user):
    # TODO permission checking
    return post.comments.all().order_by('-id')


def post__get_comments_count(post, user):
    # type: (Post, Person) -> int
    # TODO permission checking
    return post.comments.count()


def story__get_likes_count(story, user):
    # TODO permission checking
    return story.like_count


def kelaas_post__get_files(kelaas_post, user):
    # TODO permission checking
    return kelaas_post.files.all()


def conversation__get_messages(conversation, user):
    # TODO permission checking
    return conversation.messages.all().order_by('-id')


def conversation__get_last_message(conversation, user):
    # TODO permissopn checking
    return conversation.messages.all().last()


def messages__is_my_message(message, user):
    if user.id == message.writer.id:
        return True
    return False


def certificate__get_levels(certificate, user=None):
    return certificate.levels.all()


# ______________________________________________________________________________________________________
# ______________________________________________________________________________________________________

def create_kelaas(user, title, description, tags):
    if not user.type == TEACHER_KEY_WORD:
        raise myGraphQLError('Permission denied', status=403)

    kelaas = Kelaas(
        title=title,
        description=description,
    )
    kelaas.save()
    user.teacher.kelaases.add(kelaas)
    user.teacher.save()

    for tag_id in tags.split(','):
        if Tag.objects.filter(pk=tag_id).exists():
            tag = Tag.objects.get(pk=tag_id)
            kelaas.tags.add(tag)
    kelaas.save()

    return kelaas


def add_child(user, child_code):
    if not user.type == PARENT_KEY_WORD:
        raise myGraphQLError('Permission denied', status=403)

    try:
        student = Student.objects.get(parent_code=child_code)
        if student.parents:
            raise myGraphQLError('Permission denied', status=403)

        student.parents = user.parent
        student.save()
    except Student.DoesNotExist:
        raise myGraphQLError('Student not found', status=404)

    return student


def add_comment(user, post_id, body):
    try:
        post = Post.objects.get(pk=post_id)
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
        body=body,
        post_id=post_id,
        owner_id=user.id,
    )
    comment.save()
    return comment


def assign_badge(user, kelaas_id, student_id, badges):
    if not user.type == TEACHER_KEY_WORD:
        raise myGraphQLError('Permission denied', status=403)
    teacher = user.teacher

    if not teacher.kelaases.filter(pk=kelaas_id).exists():
        return False
    try:
        kelaas = user.teacher.kelaases.get(pk=kelaas_id)
        student = Student.objects.get(pk=student_id)
    except Kelaas.DoesNotExist:
        raise myGraphQLError('Kelaas not found', status=404)
    except Student.DoesNotExist:
        raise myGraphQLError('Student not found', status=404)

    for badge_id in badges.split(','):
        if Badge_link.objects.filter(student=student, type_id=badge_id, kelaas=kelaas).exists():
            t = Badge_link.objects.filter(student=student, type_id=badge_id, kelaas=kelaas).first()
            t.count = t.count + 1
            t.save()
        else:
            if not Badge.objects.filter(pk=badge_id).exists():
                raise myGraphQLError('Badge not found', status=404)
            t = Badge_link(
                student=student,
                kelaas=kelaas,
                type_id=badge_id,
            )
            t.save()
    return t


def create_kelaas_post(user, kelaas_id, title, description, files):
    if not user.type == TEACHER_KEY_WORD:
        raise myGraphQLError('Permission denied', status=403)

    try:
        kelaas = user.teacher.kelaases.get(pk=kelaas_id)
    except Kelaas.DoesNotExist:
        raise myGraphQLError('Kelaas not found', status=404)

    post = Kelaas_post(
        title=title,
        description=description,
        kelaas=kelaas,
        owner=user.teacher,
    )
    post.save()
    for file_id in files.split(','):
        if File.objects.filter(pk=file_id).exists():
            input_file = File.objects.get(pk=file_id)
            post.files.add(input_file)
    post.save()

    return post


def create_story(user, kelaas_id, title, description, pic_id=None):
    if not user.type == TEACHER_KEY_WORD:
        raise myGraphQLError('Permission denied', status=403)

    try:
        kelaas = user.teacher.kelaases.get(pk=kelaas_id)
    except Kelaas.DoesNotExist:
        raise myGraphQLError('Kelaas not found', status=404)

    story = Story(
        title=title,
        description=description,
        kelaas=kelaas,
        owner=user.teacher,
    )
    story.save()

    if pic_id:
        if File.objects.filter(pk=pic_id).exists():
            story.story_pic_id = pic_id
    story.save()
    return story


def join_kelaas(user, invite_code):
    if not user.type == STUDENT_KEY_WORD:
        raise myGraphQLError('Permission denied', status=403)

    try:
        kelaas = Kelaas.objects.get(invite_code=invite_code)
    except Kelaas.DoesNotExist:
        raise myGraphQLError('Kelaas not found', status=404)

    if not kelaas.students.filter(pk=user.id).exists():
        kelaas.students.add(user.student)
        kelaas.save()

    return kelaas


def send_message(user, conversation_id, message):
    try:
        conversation = Conversation.objects.get(pk=conversation_id)
    except Conversation.DoesNotExist:
        raise myGraphQLError('Convesation not found', status=404)

    if not conversation.members.filter(pk=user.id).exists():
        raise myGraphQLError('Permission denied', status=403)

    msg = Conversation_message(
        writer=user,
        body=message,
        conversation_id=conversation_id
    )
    msg.save()
    return msg
