from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("listing/<int:pk>", views.listing_detail, name="listing-detail"),
    path("create-listing", views.listing_create, name="listing-create"),
    path("listing/<int:pk>/close", views.listing_close, name="listing-close"),
    path("listing/<int:pk>/bid", views.bid, name="bid"),
    path("listing/<int:pk>/comment", views.comment, name="comment"),
    path("categories", views.categories, name="categories"),
    path("category/<int:pk>", views.category_detail, name="category"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("watchlist/add", views.watchlist_add, name="watchlist-create"),
    path("watchlist/remove", views.watchlist_remove, name="watchlist-remove"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
