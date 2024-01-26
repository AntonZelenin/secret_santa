from django.urls import path
from dj_rest_auth.views import LoginView, LogoutView, UserDetailsView
from webapp import api

urlpatterns = [
    path('api/register/email', api.register.email, name='webapp-register-email'),
    path('api/register/email-verification-code', api.register.verify_email, name='webapp-register-verify-email'),
    path('api/register/email/resend-verification-code', api.register.resend_email_verification_code, name='webapp-register-resend-email-verification-code'),
    path('api/register/password', api.register.password, name='webapp-register-password'),
    path('api/register/username', api.register.username, name='webapp-register-username'),

    path('api/login', LoginView.as_view(), name='webapp-login'),
    path('api/logout', LogoutView.as_view(), name='webapp-logout'),

    path('api/user', UserDetailsView.as_view(), name='webapp-user-details'),

    path('api/password/request-reset', api.password_reset.request_password_reset, name='webapp-request-password-reset'),
    path('api/password/reset', api.password_reset.reset_password, name='webapp-reset-password'),
]
