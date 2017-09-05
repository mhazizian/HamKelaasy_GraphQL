from django.conf.urls import url
from core import views

from graphene_django.views import GraphQLView

urlpatterns = [
    url(r'^$', GraphQLView.as_view(graphiql=True)),
    url(r'^graphql', views.index, name='index'),


    url(r'^' + views.Fard_API().listening_local_url + '$', views.resolve_fard, name='fard_listening'),


    url(r'^fard/temp/data$', views.temp_user_handler, name='signup'),
    url(r'^fard/register$', views.signup, name='signup'),
    url(r'^fard/login$', views.login, name='login'),

]

