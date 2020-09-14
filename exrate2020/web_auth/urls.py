from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from django.views.decorators.csrf import csrf_exempt
from . import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name="web_login"),
    path('logout/', views.LogoutView.as_view(), name="web_logout"),
    path("register/", views.RegistrationView.as_view(), name="register"),
    path("validate-username/", csrf_exempt(views.UsernameValidationView.as_view()), name="validate-username"),
    path('validate-email', csrf_exempt(views.EmailValidationView.as_view()),
         name='validate_email'),
    path('activate/<uidb64>/<token>',
         views.VerificationView.as_view(), name='web_activate'),

    path('request-reset-email/', views.PasswordResetView.as_view(),
         name="web_request-reset-email"),
    path('password-reset/<uidb64>/<token>/',
         views.SetNewPasswordView.as_view(), name='web_password-reset-confirm'),
    path('password-reset-complete', views.SetNewPasswordView.as_view(),
         name='web_password-reset-complete')
]
