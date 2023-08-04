from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('discord/', views.discord_login),
    path('discord/redirect', views.discord_login_redirect),
    path('register', views.register)
]