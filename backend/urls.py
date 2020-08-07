from django.urls import path
from . import views


urlpatterns = [
    path('cases', views.cases),
    path('numbers', views.numbers),
    path('counts', views.delta_counts),
    path('time-plot', views.time_plot),
    path('delta-plot', views.delta_plot),
    path('world-plot', views.world_plot),
    path('age-plot', views.age_plot),
]
