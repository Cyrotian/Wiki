
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('wiki/<str:page>/', views.pages, name="pages"),
    path('search/', views.search, name="search"),
    path('New_Page/', views.create_new_page, name="createNew"),
    path('Edit_Page/<str:page>', views.edit_entry, name="editEntry"),
    path('Random/', views.random_page, name="randomPage")
]
