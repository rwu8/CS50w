
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("following", views.following_view, name="following"),
    path("user/<int:user_id>", views.user_view, name="user"),
    path("register", views.register, name="register"),

    # API routes
    path("like/<int:post_id>", views.like_view, name="like"),
    path("post/<int:post_id>", views.post_view, name="post"),
]
