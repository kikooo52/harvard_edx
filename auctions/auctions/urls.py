from django.urls import path

from . import views

urlpatterns = [
    path("listing/<str:listing_id>", views.listing, name="listing"),
    path("create_comment/<str:listing_id>", views.create_comment, name="create_comment"),
    path("close/<str:listing_id>", views.close, name="close"),
    path("bookmark/<str:listing_id>", views.bookmark, name="bookmark"),
    path("category_listings/<str:id>", views.category_listings, name="category_listings"),
    path("categories", views.categories, name="categories"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("sold_listings", views.sold_listings, name="sold_listings"),
    path("create", views.create, name="create"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("", views.index, name="index"),
]
