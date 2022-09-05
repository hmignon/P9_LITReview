from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path("profile/", views.profile, name="profile"),
    path("register/", views.register, name="register"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="users/login.html"),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="users/logout.html"),
        name="logout",
    ),
    path("subscriptions/", views.subscriptions, name="subscriptions"),
    path(
        "subscriptions/confirm_unsub/<int:pk>/",
        views.UnsubscribeView.as_view(),
        name="confirm-unsub",
    ),
]
