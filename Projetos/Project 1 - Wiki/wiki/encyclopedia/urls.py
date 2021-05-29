from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<title>", views.by_title, name="entry"),
    path("new", views.new_entry, name="new"),
    path("edit/<title>", views.edit_entry, name="edit"),
    path("random", views.random_entry, name="random"),
    path("search", views.search, name="search")
]