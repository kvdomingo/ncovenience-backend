from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('api-docs', views.api_docs, name='api_docs'),
    path('api', views.api_name, name='api_name'),
    path('api/<str:page>', views.api, name='api')
]
