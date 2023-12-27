from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from django.views.generic import TemplateView

from users import views
from users.apps import UsersConfig
from users.views import RegisterView, ProfileView, reset_password, verification

app_name = UsersConfig.name


urlpatterns = [
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    #path('', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', RegisterView.as_view(template_name='users/register.html'), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('email/reset_password/', reset_password, name='reset_password'),
    path('email/verify/<str:verify_code>', verification, name='verify'),
    path('success_verify/', TemplateView.as_view(template_name='users/success_verify.html'), name='success_verify'),
    path('invalid_verify/', TemplateView.as_view(template_name='users/invalid_verify.html'), name='invalid_verify'),
]