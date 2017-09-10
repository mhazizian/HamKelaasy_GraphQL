from django.conf.urls import url
from core import views

from graphene_django.views import GraphQLView

urlpatterns = [
    # for graphql docs:
    url(r'^$', GraphQLView.as_view(graphiql=True)),

    # GraphQL main address:
    url(r'^graphql$', views.index, name='index'),

    # Upload file endpoint:
    url(r'^file/upload$', views.upload_file, name='upload'),

    # endpoint for redirecting to fard.ir with provided redirect_url
    url(r'^fard/login$', views.login, name='login'),

    # Listening url for getting data from fard.ir:
    url(r'^' + views.Fard_API().listening_local_url + '$', views.resolve_fard, name='fard_listening'),

    # endpoint for receiving data from user_temp table
    url(r'^fard/temp/data$', views.temp_user_handler, name='signup'),

    # endpoint for sending user_data for registration and getting login token
    url(r'^fard/register$', views.signup, name='signup'),

]
