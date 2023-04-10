from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import User, Listing, Bid, Comment
from .forms import ListForm
from django.contrib.auth.decorators import login_required
from decimal import Decimal

def index(request):
    return render(request, "auctions/index.html", {"listings":Listing.objects.all()})


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
def create_listing(request):
    form = ListForm()
    if request.method == "POST":
        form = ListForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.owner = request.user
            listing.save()
            return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/create.html", {"form":form})


@login_required
def listing_page(request, listing_id):
    listing = Listing.objects.get(pk=int(listing_id))

    if request.method == "POST":
        # make a comment regardless owner of listing or not
        comment = request.POST.get("comment")
        if comment:
            Comment.objects.create(owner= request.user, listing=listing, tweet=comment)
            return HttpResponseRedirect(reverse("listing_page", args=(listing.id,)))
        
        watch = request.POST.get("watch")
        if watch :
            if request.user in listing.watchlist.all():
                 listing.watchlist.remove(request.user)
            else:
                listing.watchlist.add(request.user)
        
            listing.save()
            return HttpResponseRedirect(reverse("listing_page", args=(listing.id,)))


        if request.user != listing.owner:
            value = request.POST.get("val")
            
            if value :
                try:
                    value = Decimal(value)
                except:
                    return HttpResponseBadRequest("Enter a decimal value")
                
                if value <= listing.price:
                    return HttpResponseBadRequest("Bid must be higher than current price")
                
                listing.price = value
                Bid.objects.create(listing=listing, bidder=request.user, value=value)
                listing.save()
        
        # owner of the bid 
        else:
            listing.closed = True
            listing.save()
        
        # redirection
        return HttpResponseRedirect(reverse("index"))
        
    else:
        owner_option = False
        winner = False
        ## NOTE could use len on a query set
        num = len(Bid.objects.filter(listing=listing))
        comments = Comment.objects.filter(listing=listing)
        if  request.user == listing.owner:
            owner_option = True
        
        if listing.closed:
            # filter returns whole queryset
            # no bidders would throw an error
            # get here is not safe
            try:
                bid= Bid.objects.get(listing= listing, value=listing.price)
                if bid and request.user == bid.bidder:
                    winner = True
            except:
                pass
            

        context = {"listing" : listing, 'owner_option':owner_option, 'winner':winner, "num":num, "comments":comments}
        return render(request, "auctions/listpage.html", context)


@login_required
def show_watchlist(request):
    listings = request.user.watchlist.all()
    return render(request, "auctions/watchlist.html", {"listings":listings})


def show_allcategory(request):
    cat_choices = ['Home', 'Fashion', 'Electronics', 'Toys']
    return render(request, "auctions/showcats.html", {"cat_choices":cat_choices})

def show_category(request, cat):
    listings = Listing.objects.filter(category = cat)
    return render(request, "auctions/category.html", {"cat":cat, "listings":listings})


    