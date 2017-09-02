from django.conf.urls import url
from core import views

from graphene_django.views import GraphQLView

urlpatterns = [
    url(r'^', GraphQLView.as_view(graphiql=True)),

    url(r'^test$', views.index, name='index'),
]

