from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('api', views.api_health, name='healthcheck'),
    path('api/<str:page>', views.api, name='api')
]
