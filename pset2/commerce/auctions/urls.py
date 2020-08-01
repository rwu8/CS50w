from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create", views.create_view, name="create"),
    path("category", views.category_view, name="category"),
    path("listing/<int:auction_id>", views.listing_view, name="listing"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("watchlist", views.watchlist_view, name="watchlist"),
]
