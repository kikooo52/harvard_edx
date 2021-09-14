from django.contrib.auth import authenticate, login, logout
from django.db.models import Max
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from .models import User, Listing, Bid, Comment, Category, WatchList
from .forms import ListingForm


def index(request):
    return render(request, "auctions/index.html", { 
        "listings": Listing.objects.filter(is_active=True)
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


def categories(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", { "categories": categories })


def category_listings(request, id):
    return render(request, "auctions/index.html", { 
        "listings": Listing.objects.filter(is_active=True, category__id=id)
    })


@login_required(login_url='/login')
def sold_listings(request):
    return render(request, "auctions/sold_listings.html", { 
        "listings": Listing.objects.filter(is_active=False)
    })


@login_required(login_url='/login')
def create(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            Listing.objects.create(user=request.user,
                                   title=form.cleaned_data["title"],
                                   description=form.cleaned_data["description"],
                                   price=form.cleaned_data["bid"],
                                   img_url=form.cleaned_data["img_url"],
                                   category=Category.objects.get(id=request.POST["categories"]))
    
        return HttpResponseRedirect(reverse('index'))

    else:
        form = ListingForm()
        categories = Category.objects.all()
        return render(request, "auctions/create.html", {
            "form": form,
            "categories": categories
        })


@login_required(login_url='/login')
def listing(request, listing_id):
    user = request.user
    listing = Listing.objects.get(id=listing_id)

    if request.method == "POST":
        listing.price = request.POST["bid"]
        listing.save()
        Bid.objects.create(listing=listing, user=user, price=request.POST["bid"])

    if WatchList.objects.filter(user=user, listing=listing):
        bookmark = True
    else:
        bookmark = False

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "category": listing.category,
        "comments": Comment.objects.filter(listing=listing.id), 
        "bookmark": bookmark, 
        "owner": listing.user == user
    })


@require_POST
@login_required(login_url='/login')
def create_comment(request, listing_id):
    user = request.user
    listing = Listing.objects.get(id=listing_id)    
    comment = request.POST["comment"]
    if comment:
        Comment.objects.create(user=user, listing=listing, comment=comment)

    return HttpResponseRedirect(reverse('listing', kwargs={'listing_id':listing_id}))


@login_required(login_url='/login')
def close(request, listing_id):
    listing = Listing.objects.get(id=listing_id) 
    listing.is_active = False

    bid = Bid.objects.filter(listing__id=listing_id).order_by('-price').first()
    listing.winner = str(bid.user) if bid else "No winner"
    listing.save()

    return render(request, "auctions/close.html", {
        "listing": listing,
        "category": listing.category,
        "comments": Comment.objects.filter(listing=listing.id), 
        "winner": listing.winner
    })


@login_required(login_url='/login')
def watchlist(request):
    watchlists = WatchList.objects.filter(user=request.user, listing__is_active=True)
    return render(request, "auctions/watchlist.html", {
        "watchlists": watchlists
    })


@login_required(login_url='/login')
def bookmark(request, listing_id):
    user = request.user
    listing = Listing.objects.get(id=listing_id) 
    
    try:
        watching = WatchList.objects.get(user=user, listing=listing)
    except WatchList.DoesNotExist:
        watching = None

    if watching:
        watching.delete()
        return HttpResponseRedirect(reverse('listing', kwargs={'listing_id':listing_id}))
    else:
        WatchList.objects.create(user=user, listing=listing)
        return HttpResponseRedirect(reverse('watchlist'))
    