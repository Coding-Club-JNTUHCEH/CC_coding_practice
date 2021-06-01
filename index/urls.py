from django.urls import path
from . import views

urlpatterns = [
    path('dasboard', views.dashboard_view, name='dashboard'),
    path('loadProblemsDB', views.loadProblems_view, name='load'),
    path('updateProblemsDB', views.update_solvedProblems, name='update1'),
]
