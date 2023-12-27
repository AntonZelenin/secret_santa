from django.urls import path
from webapp import views

urlpatterns = [
    path('register/', views.register, name='webapp-register'),
]
