from re import L
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from auctions.forms import BidForm, CommentForm, ListingForm

from .models import Category, User, Listing


def index(request):
    active_listings = Listing.objects.filter(is_active=True)
    return render(request, "auctions/index.html", {
        "active_listings": active_listings,
    })


def listing_detail(request, pk, *args, **kwargs):
    listing = get_object_or_404(Listing, pk=pk)
    in_watchlist = request.user.watchlist.listings.filter(pk=pk).exists()
    current_bid =  listing.bids.latest("id") if listing.bids.exists() else None
    is_current_bid_mine = current_bid.bidder == request.user if current_bid else False
    bid_form = BidForm()
    comment_form = CommentForm()
    return render(request, "auctions/detail.html", {
        "listing": listing,
        "in_watchlist": in_watchlist,
        "is_current_bid_mine": is_current_bid_mine,
        "bid_form": bid_form,
        "comment_form": comment_form,
    })


def listing_create(request):
    form = ListingForm()
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.owner = request.user
            listing.save()
            return redirect(reverse("listing-detail", kwargs={"pk": listing.pk}))
    
    return render(request, "auctions/create.html", {
        "form": form
    })


def listing_close(request):
    pass 


def bid(request, pk):
    if not request.method == "POST":
        raise Http404()
    listing = get_object_or_404(Listing, pk=pk)
    form = BidForm(request.POST)
    if form.is_valid():
        bid = form.save(commit=False)
        bid.listing = listing 
        bid.bidder = request.user
        bid.save()
    
    return redirect(reverse("listing-detail", kwargs={"pk": pk}))

def comment(request, pk):
    if not request.method == "POST":
        raise Http404()
    
    listing = get_object_or_404(Listing, pk=pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.listing = listing 
        comment.user = request.user
        comment.save()
    
    return redirect(reverse("listing-detail", kwargs={"pk": pk}))


def categories(request):
    category_list = Category.objects.all()
    return render(request, "auctions/categories.html", {
        "categories": category_list
    })

def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    return render(request, "auctions/category.html", {
        "category": category
    })

def watchlist(request):
    
    return render(request, "auctions/watchlist.html", {
        "watchlist": request.user.watchlist
    })

def watchlist_add(request):
    pass 

def watchlist_remove(request):
    pass 


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
