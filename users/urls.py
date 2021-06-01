from django.urls import path
from . import views

urlpatterns = [
    path('signup', views.signup_view, name='signup'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('users/<str:username>', views.profile_view, name='profile'),
    path('users', views.profile_view, name='profile'),
    path('edit-profile', views.editProfile_view, name='edit_profile'),
    path('addSolvedProblems', views.addSolvedProblems, name='addProblems'),
    path('edit-profile/change-password',
         views.changePassword_view, name='changePassword_view'),
]
