from django.urls import path
from . import views


urlpatterns = [
    path('', views.honeypot_login, name='home'),
]
