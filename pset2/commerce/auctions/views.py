from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import User, Category, Auction, Comment, WatchList


class NewListingForm(forms.Form):
    title = forms.CharField(label="Title")
    description = forms.CharField(widget=forms.Textarea, label="Description")
    starting_bid = forms.FloatField(label="Bid")
    starting_bid.widget.attrs.update({'step': 'any'})
    categories = Category.objects.all()
    photo = forms.CharField(label="Link to Image")

    def __init__(self, *args, **kwargs):
        super(NewListingForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


def category_view(request):
    categories = Category.objects.all()
    
    if request.method == "POST":
        category = Category.objects.get(pk=request.POST['category'])
        auctions = Auction.objects.filter(category=category)
        
        return render(request, "auctions/category.html", {
            "categories": categories,
            "category": category,
            "auctions": auctions
        })
    else:
        listing = NewListingForm()
        categories = listing.categories
        return render(request, "auctions/category.html", {
            "categories": categories
        })


@login_required
def create_view(request):
    # user submitted form for new auction
    if request.method == "POST":
        category = Category.objects.get(pk=request.POST['category'])
        new_auction = Auction(title=request.POST['title'], description=request.POST['description'], starting_price=float(request.POST['starting_bid']), listing_user = request.user, current_price_user = None, winning_user = None, category = category, photo = request.POST['photo'], is_closed = False)
        new_auction.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        listing = NewListingForm()
        categories = listing.categories
        return render(request, "auctions/create.html", {
            "form": listing,
            "categories": categories
        })


def index(request):
    open_auction = Auction.objects.filter(is_closed=False)
    return render(request, "auctions/index.html", {
        "auctions": open_auction
    })


def listing_view(request, auction_id):
    auction = Auction.objects.get(pk=auction_id)
    comments = Comment.objects.filter(auction=auction)

    if request.method == "POST":
        # check to see if current user is watching the item
        try:
            is_watching = auction.filter_watchlist_auction.get(user=request.user)
        except:
            is_watching = False

        if 'bid_amount' in request.POST:
            if request.POST["bid_amount"]:
                # if first bid
                if not auction.current_price:
                    # low bid, must be at least equal to the starting bid
                    if not float(request.POST["bid_amount"]) >= auction.listing_price:
                        return render(request, "auctions/listing.html", {
                            "auction": auction,
                            "comments": comments,
                            "message": None,
                            "is_watching": is_watching,
                            "authenticated": True,
                            "message": "low_bid",
                            "user": request.user
                        })
                    else:
                        auction.current_price = float(request.POST["bid_amount"])
                        auction.current_price_user = request.user
                        auction.save()
                        return render(request, "auctions/listing.html", {
                            "auction": auction,
                            "comments": comments,
                            "message": "bid",
                            "is_watching": is_watching,
                            "authenticated": True,
                            "user": request.user
                        })
                
                else:
                    # low bid, must be greater than the current bid
                    if not float(request.POST["bid_amount"]) > auction.current_price:                    
                        return render(request, "auctions/listing.html", {
                            "auction": auction,
                            "comments": comments,
                            "is_watching": is_watching,
                            "authenticated": True,
                            "message": "low_bid",
                            "user": request.user
                        })
                    # update the current_price and current_price_user with the new bid information
                    else:
                        auction.current_price = float(request.POST["bid_amount"])
                        auction.current_price_user = request.user
                        auction.save()
                        return render(request, "auctions/listing.html", {
                            "auction": auction,
                            "comments": comments,
                            "message": "bid",
                            "is_watching": is_watching,
                            "authenticated": True,
                            "user": request.user
                        })

        if 'close_auction' in request.POST:
            # close the auction and set the winning_user to the current_price_user
            if request.POST["close_auction"] and not auction.is_closed:
                auction.is_closed = True
                auction.winning_user = auction.current_price_user
                auction.save()
                return render(request, "auctions/listing.html", {
                            "auction": auction,
                            "comments": comments,
                            "message": None,
                            "is_watching": is_watching,
                            "authenticated": True,
                            "user": request.user
                })
        
        if 'remove_watch_auction' in request.POST:
            if request.POST["remove_watch_auction"]:
                watchlist = WatchList.objects.get(user=request.user, auction=auction)
                # print("REMOVING", watchlist)
                watchlist.delete()
                return render(request, "auctions/listing.html", {
                            "auction": auction,
                            "comments": comments,
                            "message": None,
                            "is_watching": False,
                            "authenticated": True,
                            "user": request.user
                })

        if 'add_watch_auction' in request.POST:    
            if request.POST["add_watch_auction"]:
                new_watchlist_item = WatchList(user=request.user, auction=auction)
                print("ADDING", new_watchlist_item)
                new_watchlist_item.save()
                return render(request, "auctions/listing.html", {
                            "auction": auction,
                            "comments": comments,
                            "message": None,
                            "is_watching": True,
                            "authenticated": True,
                            "user": request.user
                })
        
        if 'add_comment' in request.POST:    
            if request.POST["add_comment"]:
                new_comment = Comment(user=request.user, auction=auction, comment=request.POST["add_comment"])
                new_comment.save()
                comments = Comment.objects.filter(auction=auction)
                return render(request, "auctions/listing.html", {
                            "auction": auction,
                            "comments": comments,
                            "message": None,
                            "is_watching": is_watching,
                            "authenticated": True,
                            "user": request.user
                })
    
    # method is GET
    else:
        if request.user.is_authenticated:
            authenticated = True
            try:
                # check to see if current user is watching the item
                is_watching = WatchList.objects.get(user=request.user, auction=auction)
                # print(is_watching)
            except:
                is_watching = False
        else:
            authenticated = False
            is_watching = False

        print(auction.listing_user, request.user)
        return render(request, "auctions/listing.html", {
            "auction": auction,
            "comments": comments,
            "message": None,
            "is_watching": is_watching,
            "authenticated": authenticated,
            "user": request.user
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


@login_required
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
def watchlist_view(request):
    # Ensure user is logged in
    if request.user.is_authenticated:
        auctions = []
        watchlist = WatchList.objects.filter(user=request.user)
        
        for auction in watchlist:
            auctions.append(Auction.objects.get(pk=auction.auction.id))

        return render(request, "auctions/watchlist.html", {
            "auctions": auctions
        })
    else:
        return HttpResponseRedirect(reverse("index"))