from django.conf.urls import url
from core import views

from graphene_django.views import GraphQLView

urlpatterns = [
    url(r'^test$', views.test, name='index'),
    url(r'^index$', views.index, name='index'),



    url(r'^register$', views.signup, name='signup'),
    url(r'^$', GraphQLView.as_view(graphiql=True)),

]

