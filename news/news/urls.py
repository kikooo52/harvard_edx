from django.urls import path

from . import views

urlpatterns = [
    path("create", views.create, name="create"),
    path("create_comment/<int:news_id>", views.create_comment, name="create_comment"),
    path("edit_news/<int:news_id>", views.edit_news, name="edit_news"),
    path('bookmarked_news/<int:user_id>', views.bookmarked_news, name='bookmarked_news'),
    path('bookmark_news/<int:news_id>', views.bookmark_news, name='bookmark_news'),
    path("news_detail/<str:slug>", views.news_detail, name="news_detail"),
    path("category_news/<int:id>", views.category_news, name="category_news"),
    path("categories", views.categories, name="categories"),
    path("europe_news", views.europe_news, name="europe_news"),
    path("world_news", views.world_news, name="world_news"),
    path("sport_news", views.sport_news, name="sport_news"),
    path("profile/<int:user_id>", views.profile, name="profile"),
    path('search_news/', views.search_news, name='search_news'),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("", views.index, name="index"),
]
