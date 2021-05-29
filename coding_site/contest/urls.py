from django.urls import path
from . import views

urlpatterns = [
    path('contest', views.contest_page, name='contest_page'),
    path('contest-all', views.contest_page, name='contest_page'),
    path('contest/<str:type1>', views.contest_page, name='contest_page'),
    path('loadContestsDB', views.loadContests_view, name='load'),
    path('updateContestProblemsDB', views.update_contestProblems, name='updatee')
]