from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create"),
    path("watchlist", views.show_watchlist, name="watchlist"),
    path("category", views.show_allcategory, name="categories"),
    path("category/<str:cat>", views.show_category, name="category"),
    path("<int:listing_id>", views.listing_page, name="listing_page")
]
