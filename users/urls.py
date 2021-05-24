from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('signup', views.signup_view, name = 'signup'),
    path('login', views.login_view, name = 'login'),
    path('help-codeforces', views.help_CF_view, name = 'help'),
    path('logout', views.logout_view, name = 'logout'),
    path('users/<str:username>', views.profile_view, name = 'profile'),
    path('users', views.profile_view, name = 'profile'),
    path('edit-profile', views.editProfile_view, name = 'edit_profile'),
    path('edit-profile/change-password', views.changePassword_view, name = 'changePassword_view'),

    path('reset-password', 
        auth_views.PasswordResetView.as_view(template_name = 'password_reset/password_reset.html'),
        name = 'reset_password'),
    path('reset-password-sent', 
        auth_views.PasswordResetDoneView.as_view(template_name="password_reset/password_reset_sent.html"), 
        name='password_reset_done'),
    path('reset/<uidb64>/<token>', 
        auth_views.PasswordResetConfirmView.as_view(template_name="password_reset/password_reset_form.html"), 
        name = 'password_reset_confirm'),
    path('reset-password', 
        auth_views.PasswordResetView.as_view(template_name="password_reset/password_reset_done.html"), 
        name = 'password_reset_complete'),
]