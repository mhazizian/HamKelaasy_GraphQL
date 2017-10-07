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

    # endpoint for redirecting to fard.ir with provided redirect_url
    url(r'^fard/login$', views.login),
    url(r'^fard/login/$', views.login),

    # endpoint for sending user_data for registration and getting login token
    url(r'^fard/register$', views.signup, name='signup'),
    url(r'^fard/register/$', views.signup),

    # endpoint for receiving data from user_temp table
    url(r'^fard/temp/data$', views.temp_user_handler, name='signup'),
    url(r'^fard/temp/data/$', views.temp_user_handler),

    # Listening url for getting data from fard.ir:
    url(r'^' + views.Fard_API().listening_local_url + '$', views.resolve_fard, name='fard-listening'),

    # for getting besic kelaas information using kelaas invite code
    url(r'^kelaas/basic_info$', views.get_kelaas_basic_info_handler, name='kelaas-basic-information'),
    url(r'^kelaas/basic_info/$', views.get_kelaas_basic_info_handler),

    url(r'^apply$', views.my_view, name='test'),
    url(r'^apply/$', views.my_view),


    url(r'^register/phone/sendvalidation$', views.get_phone_number, name='get-phone-number'),
    url(r'^register/phone/sendvalidation/$', views.get_phone_number),

    url(r'^register/phone/validate$', views.validate_phone_number, name='validate-phone-number'),
    url(r'^register/phone/validate/$', views.validate_phone_number,),

    url(r'^register/parent$', views.new_signup_parent, name='signup-parent'),
    url(r'^register/parent/$', views.new_signup_parent, name='signup-parent'),

    url(r'^register/teacher$', views.new_signup_teacher, name='signup-teacher'),
    url(r'^register/teacher/$', views.new_signup_teacher),

    url(r'^register/student/basicInfo$', views.get_student_basic_info, name='signup-student-basic-info'),
    url(r'^register/student/basicInfo/$', views.get_student_basic_info),

    url(r'^login$', views.new_login, name='login'),
    url(r'^login/$', views.new_login),

    url(r'^reset/password$', views.reset_password, name='reset-password'),
    url(r'^reset/password/$', views.reset_password),
]
