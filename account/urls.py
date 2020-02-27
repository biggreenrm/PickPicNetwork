from django.urls import path
from . import views

urls = [
    path("login/", views.user_login, name="login"),
]
