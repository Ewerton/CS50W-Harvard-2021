from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_listing", views.new_listing, name="new_listing"),
    path("listing/<str:listing_id>", views.listing, name="listing"),
    path("remove_watchlist/<str:listing_id>", views.remove_watchlist, name="remove_watchlist"),
    path("add_watchlist/<str:listing_id>", views.add_watchlist, name="add_watchlist"),
    path("bidding/<str:listing_id>", views.bidding, name="bidding"),
    path("close_bidding/<str:listing_id>", views.close_bidding, name="close_bidding"),
    path("remove_listing/<str:listing_id>", views.remove_listing, name="remove_listing"),
    path("watch_list", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path("by_category/<str:category_id>", views.by_category, name="by_category"),
    path("my_listings", views.my_listings, name="my_listings"),
    path("search", views.search, name="search")
]
