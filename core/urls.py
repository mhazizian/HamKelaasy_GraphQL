from django.conf.urls import url
from core import views

from graphene_django.views import GraphQLView

urlpatterns = [
    # for graphql docs:
    url(r'^$', GraphQLView.as_view(graphiql=True)),

    # GraphQL main address:
    url(r'^graphql$', views.index, name='index'),
    url(r'^graphql/$', views.index),

    # logout url
    url(r'^logout$', views.logout, name='logout'),
    url(r'^logout/$', views.logout),

    # Upload file endpoint:
    url(r'^file/upload$', views.upload_file, name='upload'),
    url(r'^file/upload/$', views.upload_file),

    # for getting besic kelaas information using kelaas invite code
    url(r'^kelaas/basic_info$', views.get_kelaas_basic_info_handler, name='kelaas-basic-information'),
    url(r'^kelaas/basic_info/$', views.get_kelaas_basic_info_handler),

    url(r'^register/phone/sendvalidation$', views.get_phone_number, name='get-phone-number'),
    url(r'^register/phone/sendvalidation/$', views.get_phone_number),

    url(r'^register/phone/validate$', views.validate_phone_number, name='validate-phone-number'),
    url(r'^register/phone/validate/$', views.validate_phone_number, ),

    url(r'^register/parent$', views.new_signup_parent, name='signup-parent'),
    url(r'^register/parent/$', views.new_signup_parent, name='signup-parent'),

    url(r'^register/teacher$', views.new_signup_teacher, name='signup-teacher'),
    url(r'^register/teacher/$', views.new_signup_teacher),

    url(r'^register/student/getBasicInfo$', views.get_student_basic_info, name='signup-student-basic-info'),
    url(r'^register/student/getBasicInfo/$', views.get_student_basic_info),

    url(r'^register/student$', views.new_signup_student, name='signup-student'),
    url(r'^register/student/$', views.new_signup_student),

    url(r'^register/student/code$', views.new_signup_student_by_code, name='signup-student'),
    url(r'^register/student/code/$', views.new_signup_student_by_code),

    url(r'^login$', views.new_login, name='login'),
    url(r'^login/$', views.new_login),

    url(r'^login/phone$', views.login_by_phone, name='login-by-phone'),
    url(r'^login/phone/$', views.login_by_phone),

    url(r'^reset/password/by_phone$', views.reset_password, name='reset-password'),
    url(r'^reset/password/by_phone/$', views.reset_password),

    url(r'^register/migrate$', views.migrate_user, name='migrate'),
    url(r'^register/migrate/$', views.migrate_user),

    url(r'^info$', views.info, name='info'),
    url(r'^info/$', views.info),

    url(r'^docs/errors$', views.error_doc, name='error-doc'),
    url(r'^docs/errors/$', views.error_doc),

    url(r'^docs/notifications$', views.notification_doc, name='notification-doc'),
    url(r'^docs/notifications/$', views.notification_doc),

    url(r'^apply$', views.my_view, name='test'),
    url(r'^apply/$', views.my_view),
]
