from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('data', views.data, name='data'),
    path('api', views.api, name='api'),
    path('api/geo', views.api_geo, name='geo'),
]
