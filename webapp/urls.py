from django.urls import path
from webapp.api import register

urlpatterns = [
    path('api/register/email', register.email, name='webapp-register-email'),
    path('api/register/email-verification-code', register.verify_email, name='webapp-register-verify-email'),
    # todo maybe a bad url
    path('api/register/email/resend-verification-code', register.resend_email_verification_code, name='webapp-register-resend-email-verification-code'),
    path('api/register/password', register.password, name='webapp-register-password'),
    path('api/register/username', register.username, name='webapp-register-username'),
]
