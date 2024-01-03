from django.urls import path
from webapp.api import register

urlpatterns = [
    path('register/email', register.email, name='webapp-register-email'),
]
