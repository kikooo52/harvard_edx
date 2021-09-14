from django.urls import path

from . import views

urlpatterns = [
    path('random_page', views.random, name='random_page'),
    path('wiki/<str:title>', views.detail, name='wiki'),
    path('create', views.create, name='create'),
    path('check_entry/<str:title>', views.check_entry, name='check_entry'),
    path('edit/<str:title>', views.edit, name='edit'),
    path('search/', views.search_results, name='search_results'),
    path('', views.index, name="index"),
]
