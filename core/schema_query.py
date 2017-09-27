import graphene
import core.services as services
from core import myGraphQLError
from graphql_query import *


def resolve_student(root, info, **kwargs):
    if not info.context.user.is_authenticated:
        raise myGraphQLError('user not authenticated', status=401)
    user = info.context.user.person
    return services.get_student(user=user, **kwargs)


def resolve_students(root, info, page, page_size, **kwargs):
    if not info.context.user.is_authenticated:
        raise myGraphQLError('user not authenticated', status=401)
    user = info.context.user.person

    query_set = services.get_students(user=user, **kwargs)
    return services.apply_pagination(query_set, page=page, page_size=page_size)


def resolve_kelaas(root, info, id):
    if not info.context.user.is_authenticated:
        raise myGraphQLError('user not authenticated', status=401)
    user = info.context.user.person

    return services.get_kelaas(user=user, kelaas_id=id)


def resolve_kelaases(root, info, page, page_size, **kwargs):
    if not info.context.user.is_authenticated:
        raise myGraphQLError('user not authenticated', status=401)
    user = info.context.user.person

    query_set = services.get_kelaases(user=user, **kwargs)
    return services.apply_pagination(query_set, page=page, page_size=page_size)


def resolve_teacher(root, info):
    if not info.context.user.is_authenticated:
        raise myGraphQLError('user not authenticated', status=401)
    user = info.context.user.person

    return services.get_teacher(user)


def resolve_parent(root, info, **kwargs):
    if not info.context.user.is_authenticated:
        raise myGraphQLError('user not authenticated', status=401)
    user = info.context.user.person

    return services.get_parent(user, **kwargs)


def resolve_me(root, info):
    if not info.context.user.is_authenticated:
        raise myGraphQLError('user not authenticated', status=401)
    # TODO: move this func to business logic
    return info.context.user.person


def resolve_badge_types(root, info, page, page_size, **kwargs):
    query_set = services.get_badge_types(**kwargs)
    return services.apply_pagination(query_set, page=page, page_size=page_size)


def resolve_certificate(root, info, id):
    return services.get_certificate(id)


def resolve_tags(root, info):
    return services.get_tags()


def resolve_conversation(root, info, id):
    if not info.context.user.is_authenticated:
        raise myGraphQLError('user not authenticated', status=401)
    user = info.context.user.person

    return services.get_conversation(user=user, conversation_id=id)


def resolve_system_notifications(root, info, page, page_size, new):
    if not info.context.user.is_authenticated:
        raise myGraphQLError('user not authenticated', status=401)
    user = info.context.user.person

    query_set = services.get_system_notifications(user=user, new=new)
    return services.apply_pagination(query_set, page=page, page_size=page_size)


# Query class:
class Query(graphene.ObjectType):
    me = graphene.Field(
        PersonType,
        description="Authentication required.\n\nreturn basic info about the registered user.",
        resolver=resolve_me,
    )

    student = graphene.Field(
        StudentType,
        description="Authentication required.\n\nif registered as student, returns current user",
        id=graphene.Int(description="Parent and Teacher: 'id' is necessary. 'id' refers to student_id"),
        resolver=resolve_student,
    )

    students = graphene.List(
        StudentType,
        description="Authentication required.\n\nParent: return all childrens.\n\n"
                    + "Teacher: a 'kelaas_id' is necessary and return all students on that kelaas,",
        page_size=graphene.Int(default_value=services.DEFAULT_PAGE_SIZE),
        page=graphene.Int(default_value=1),
        kelaas_id=graphene.Int(description="necessary for Teacher"),
        resolver=resolve_students,
    )
    teacher = graphene.Field(
        TeacherType,
        description="Authentication required.\n\nonly if current user is a teacher.",
        resolver=resolve_teacher
    )

    parent = graphene.Field(
        ParentType,
        description="Authentication required.\n\n"
                    "if registered as parent, returns current user.\n\n"
                    "if registered as teacher, parent_id is necessary and return parent only if has access to him.",
        resolver=resolve_parent,
        id=graphene.Int(description="Parent id.(required if current user is teacher)"),
    )

    kelaas = graphene.Field(
        KelaasType,
        description="Authentication required.\n\n",
        id=graphene.Int(required=True, description="kelaas id."),
        resolver=resolve_kelaas,
    )

    kelaases = graphene.List(
        KelaasType,
        description="Authentication required.\n\nTeacher: return all teacher's kelaases.\n\n"
                    + "Parent: 'student_id' is necessary and return all of student's kelaases,\n\n"
                    + "(only of parent has access to student)",
        page_size=graphene.Int(default_value=services.DEFAULT_PAGE_SIZE),
        page=graphene.Int(default_value=1),
        student_id=graphene.Int(description="necessary for parents. return all of student's kelaases,"),
        resolver=resolve_kelaases,
    )

    certificate = graphene.Field(
        CertificateType,
        description="Certificate info for certificate page.",
        id=graphene.Int(required=True, description="Certificate id."),
        resolver=resolve_certificate,
    )

    tags = graphene.List(
        TagType,
        description="returns 'all' tags registered in system.",
        resolver=resolve_tags,
    )

    badge_types = graphene.List(
        BadgeModelType,
        description="returns all badges registered in system.\n\n(usage: showing to teacher on assigning page)",
        id=graphene.Int(description="optional, if provided: return badge with related badge_id"),
        page_size=graphene.Int(default_value=services.DEFAULT_PAGE_SIZE),
        page=graphene.Int(default_value=1),
        resolver=resolve_badge_types,
    )

    conversation = graphene.Field(
        ConversationType,
        id=graphene.Int(
            required=True,
            description="conversation id"
        ),
        description="Returns Conversation only if current user has access to it",
        resolver=resolve_conversation,
    )
    system_notifications = graphene.List(
        SystemNotificationType,
        page_size=graphene.Int(default_value=services.DEFAULT_PAGE_SIZE),
        page=graphene.Int(default_value=1),
        new=graphene.Boolean(
            default_value=False,
            description="if True, only returns new system_notification(default = False)",
        ),
        description="Returns System notification",
        resolver=resolve_system_notifications,
    )
