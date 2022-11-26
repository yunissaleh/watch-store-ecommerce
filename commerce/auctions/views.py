from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Category, Listings, Comments, Bids


def index(request):
    return render(request, "auctions/index.html", {
        "listing": Listings.objects.filter(active=True),
        "header": "Active Listings"

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


def newListing(request):
    if request.method == "GET":
        return render(request, "auctions/newListing.html", {
            "categories": Category.objects.all()
        })
    elif request.method == "POST":
        title = request.POST['title']
        user = request.user
        img = request.POST['imageUrl']
        description = request.POST['description']
        price = request.POST['price']
        category_id = int(request.POST["category"])

        category = Category.objects.get(pk=category_id)

        listing = Listings(title=title, seller_name=user, image=img, description=description,
                           startingPrice=float(price),
                           category=category)
        listing.save()
        return HttpResponseRedirect(reverse(index))


def listing(request, id):
    listed = Listings.objects.get(pk=id)
    comments = Comments.objects.filter(title=listed)
    isSeller = request.user.username == listed.seller_name.username
    bids = Bids.objects.filter(listing=listed)

    global buyer
    buyer = ""
    for bid in bids:
        if bid.offer == listed.currentPrice:
            buyer = bid.bidder
        # else:
        #     buyer = ""
    return render(request, "auctions/listing.html", {
        "listing": listed,
        "checkWatchlist": request.user in listed.watchlisters.all(),
        "comments": comments,
        "comments_num": comments.count(),
        "isSeller": isSeller,
        "buyer": buyer
    })


def addBid(request, id):
    listed = Listings.objects.get(pk=id)
    comments = Comments.objects.filter(title=listed)
    bid = float(request.POST['bid'])
    if (listed.currentPrice is None or bid > listed.currentPrice) and bid >= listed.startingPrice:
        listed.currentPrice = bid
        newBid = Bids(listing=listed, bidder=request.user, offer=bid)
        newBid.save()
        listed.save()
        return HttpResponseRedirect(reverse("listing", args=(id,)))
    else:
        return render(request, "auctions/listing.html", {
            "listing": listed,
            "checkWatchlist": request.user in listed.watchlisters.all(),
            "comments": comments,
            "comments_num": comments.count(),
            "status": True
        })


def closeListing(request, id):
    listed = Listings.objects.get(pk=id)
    listed.active = False
    listed.save()
    comments = Comments.objects.filter(title=listed)
    isSeller = request.user.username == listed.seller_name.username

    return render(request, "auctions/listing.html", {
        "listing": listed,
        "checkWatchlist": request.user in listed.watchlisters.all(),
        "comments": comments,
        "comments_num": comments.count(),
        "isSeller": isSeller,
    })


def addWatch(request, id):
    Listings.objects.get(pk=id).watchlisters.add(request.user)
    return HttpResponseRedirect(reverse("listing", args=(id,)))


def removeWatch(request, id):
    Listings.objects.get(pk=id).watchlisters.remove(request.user)
    return HttpResponseRedirect(reverse("listing", args=(id,)))


def watchlist(request):
    return render(request, "auctions/index.html", {
        "listing": request.user.watchlist.all(),
        "header": "Watchlist"
    })


def postComment(request, id):
    if request.method == "POST":
        listing = Listings.objects.get(pk=id)
        content = request.POST['comment']
        commenter = request.user
        comment = Comments(title=listing, commenter=commenter, content=content)
        comment.save()
        return HttpResponseRedirect(reverse("listing", args=(id,)))


def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": Category.objects.all()
    })


def categoryIndex(request, name):
    return render(request, "auctions/index.html", {
        "listing": Listings.objects.filter(category=Category.objects.get(type=name), active=True),
        "header": name

    })
