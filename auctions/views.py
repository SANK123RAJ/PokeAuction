from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from datetime import datetime
from django.contrib.auth.decorators import login_required
from .models import *

from .models import User


def iswatchlisted(request,id): 
    iswatchlisted = False
    if request.user.is_authenticated :
        watchlistsofuser = request.user.user.all()
        if Listings.objects.get(pk = (id)) in watchlistsofuser:
            iswatchlisted = True
    return iswatchlisted

def bidder(listingid):
    Listin = Listings.objects.get(pk = listingid)
    bid = Listin.bid.all()
    if len(bid) != 0:
     bidby = bid[len(bid)-1].bid_by.username
     return bidby
    else:
        return "To_be_Bid"

def allcomments(listingid):
    Listin = Listings.objects.get(pk = listingid)
    comments = Listin.allcomment.all()
    if len(comments)!=0:
        return comments
    


now  = datetime.now()
def index(request):
    return render(request, "auctions/index.html",{
        "Listing": Listings.objects.all(),
        "mode": "Alllisting",
        "categorylist": category.objects.all()
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
@login_required
def addlisting(request):
    if request.method == "POST":
        new_entry = Listings()
        new_entry.name = request.POST["Name"]
        new_entry.description = request.POST["description"]
        new_entry.price = request.POST["price"]
        new_entry.time = now
        new_entry.url = request.POST["url"]
        new_entry.category = category.objects.get(categoryname = request.POST["category"])
        new_entry.owner = User.objects.get(username = request.user.username)
        new_entry.save()
        return render(request,"auctions/addlisting.html",{
        "categories": category.objects.all(),
        "message": "Your Listing Added Successfully"
    })
        



    return render(request,"auctions/addlisting.html",{
        "categories": category.objects.all()
    })

def listing(request,id):
     return render(request, "auctions/listing.html",{
        "Listing": Listings.objects.get(pk = (id)),
        "watchlisted": iswatchlisted(request,id),
        "bidder": bidder(id),
        "comments" : allcomments(id),
        "categorylist": category.objects.all()

    })

@login_required
def watchlist(request,listingid):
    instance = Listings.objects.get(pk=listingid)
    instance.watchlist.add(request.user)
    instance.save()
    
    return render(request, "auctions/listing.html",{
        "Listing": Listings.objects.get(pk = (listingid)),
        "message": (Listings.objects.get(pk = (listingid))).name + " Added to Your WatchList !",
        "Success": True,
        "watchlisted": iswatchlisted(request,listingid),
        "bidder": bidder(listingid),
        "comments" : allcomments(listingid),
        "categorylist": category.objects.all()
    })

@login_required
def displaywatchlist(request):
    userworking = User.objects.get(username = request.user.username)
    alllists = userworking.user.all()
    return render(request, "auctions/index.html",{
        "watchlists": alllists,
        "mode": "WatchList",
        "categorylist": category.objects.all()
    })

@login_required
def removewatchlist(request,listingid):
    instance = Listings.objects.get(pk=listingid)
    instance.watchlist.remove(request.user)
    instance.save()
    
    return render(request, "auctions/listing.html",{
        "Listing": Listings.objects.get(pk = (listingid)),
        "message": (Listings.objects.get(pk = (listingid))).name + " Removed from Your WatchList !",
        "Success": False,
        "watchlisted": iswatchlisted(request,listingid),
        "bidder": bidder(listingid),
        "comments" : allcomments(listingid),
        "categorylist": category.objects.all()
    })

@login_required
def addbid(request,listingid):
    if request.method == "POST":
        if request.POST["Submit"] == 'False':
            return render(request, "auctions/listing.html",{
        "Listing": Listings.objects.get(pk = (listingid)),
        "watchlisted": iswatchlisted(request,listingid),
        "Form": True,
        "bidder": bidder(listingid),
        "comments" : allcomments(listingid),
        "categorylist": category.objects.all()
    })
        else:
            if int(request.POST["bid"]) >= (Listings.objects.get(pk = listingid)).price :
                newbid = Bids()
                newbid.amount = int(request.POST["bid"])
                newbid.biddedlist = Listings.objects.get(id = listingid) 
                newbid.bid_by = request.user
                newbid.save()
                instance = Listings.objects.get(pk = listingid)
                instance.price = int(request.POST["bid"])
                instance.save()
                return render(request, "auctions/listing.html",{
        "Listing": Listings.objects.get(pk = (listingid)),
        "message": "Bid Placed Successfully!",
        "Success": True,
        "watchlisted": iswatchlisted(request,listingid),
        "bidder": bidder(listingid),
        "comments" : allcomments(listingid),
        "categorylist": category.objects.all()
    })
            else:
                return render(request, "auctions/listing.html",{
        "Listing": Listings.objects.get(pk = (listingid)),
        "message": "Error! Couldnt Place Your Bid",
        "Success": False,
        "watchlisted": iswatchlisted(request,listingid),
        "Form": True,
        "bidder": bidder(listingid),
        "comments" : allcomments(listingid),
        "categorylist": category.objects.all()
    })

@login_required
def closebid(request,listingid):
    currentlisting = Listings.objects.get(pk = listingid)
    currentlisting.isactive = False
    currentlisting.save()
    return HttpResponseRedirect(reverse(listing, args=(listingid,)))

@login_required
def addcomment(request,listingid):
    if request.method == "POST":
        instance = Comment()
        instance.commentmade = request.POST["comment"]
        instance.commentby = request.user
        instance.commenton = Listings.objects.get(pk = listingid)
        instance.save()
        return HttpResponseRedirect(reverse(listing, args=(listingid,)))
    


def displaycategory(request):
    if request.method == "POST":
        
        categoryid = request.POST["categoryid"]
        categorryselected = category.objects.get(pk = int(categoryid))
        alllists = categorryselected.category.all()
        
        return render(request, "auctions/index.html",{
        "currentcategorylist": alllists,
        "mode": "CategoryList",
        "categorylist": category.objects.all()
        })
    else:
        return HttpResponse("ERROR")


               

    


