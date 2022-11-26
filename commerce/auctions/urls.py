from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newListing", views.newListing, name="newListing"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("addWatch/<int:id>", views.addWatch, name="add"),
    path("removeWatch/<int:id>", views.removeWatch, name="remove"),
    path("addBid/<int:id>", views.addBid, name="addBid"),
    path("postComment/<int:id>", views.postComment, name="postComment"),
    path("closeListing/<int:id>", views.closeListing, name="closeListing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:name>", views.categoryIndex, name="categoryIndex")
]
