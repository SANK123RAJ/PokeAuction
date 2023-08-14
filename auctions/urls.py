from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("addlisting", views.addlisting, name = "addlisting"),
    path("<int:id>/listing", views.listing, name = "listing"),
    path("<int:listingid>/watchlist", views.watchlist, name = "watchlist"),
    path("<int:listingid>/removewatchlist", views.removewatchlist, name = "removewatchlist"),
    path("watchlist", views.displaywatchlist, name = "Displaywatchlist"),
    path("<int:listingid>/addbid",views.addbid, name = "addbid"),
    path("<int:listingid>/closebid",views.closebid, name = "closebid"),
    path("<int:listingid>/addcomment",views.addcomment, name = "addcomment"),
    path("category",views.displaycategory, name = "displaycategory")
    
    

]
