from django.urls import path
from . import views

urlpatterns = [
    path("wiki/", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("wiki/create/", views.create, name="create"),
    path("wiki/edit/<str:title>", views.edit_page, name="edit"),
    path("wiki/random/", views.random_page, name="random"),
]
