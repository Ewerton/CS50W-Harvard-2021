from auctions.ListingInfo import ListingInfo
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.http import is_safe_url
from django.db.models import Q
from django.db.models import Max
from django.db.models import Count

from .models import User, Listing, Bid, Comment, Category, WatchList
from .forms import NewListingForm


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(sold=False)
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
            # redirect the user to the previous URL saved in the session that could be the "/" or some custom location
            return HttpResponseRedirect(request.session['redirect_to'])
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        #try to identify if the user should be redirected to some specific page after the login
        redirect_to = request.GET.get('next')
        if (redirect_to == None ):
            redirect_to = reverse("index")
        
        request.session['redirect_to'] = redirect_to
        
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    
    # Sets a default return URL for the subsequents logins
    request.session['redirect_to'] = reverse("index")
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
        return HttpResponseRedirect(request.session['redirect_to'])
    else:
        #try to identify if the user should be redirected to some specific page after the login
        redirect_to = request.GET.get('next')
        if (redirect_to == None ):
            redirect_to = reverse("index")
        
        request.session['redirect_to'] = redirect_to
 
        return render(request, "auctions/register.html")

@login_required
def new_listing(request):
    if request.method == "POST":
        form = NewListingForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            bid = form.cleaned_data["start_bid"]
            image_url = form.cleaned_data["image_url"]
            user = request.user
            category_id = Category.objects.get(id=form.cleaned_data["category"])
            Listing.objects.create(
                    user = user, 
                    title = title, 
                    description = description, 
                    price = bid, 
                    image_url = image_url, 
                    category = category_id)
    
        return HttpResponseRedirect(reverse('index'))

    else:
        return render(request, "auctions/new_listing.html", {
            "listing_form": NewListingForm(),
            "categories": Category.objects.all()
        })

def listing(request, listing_id):
    listing_info = ListingInfo(request, listing_id)

    # User posting a comment
    if request.method == "POST":
        comment = request.POST["comment"]
        if comment != "":
            Comment.objects.create(user = request.user, listing = listing_info.listing, comment = comment)    

    return render(request, "auctions/listing.html", {
        "listing": listing_info.listing,
        "category": listing_info.category,
        "comments": listing_info.comments, 
        "is_watching": listing_info.is_watching, 
        "is_owner": listing_info.is_owner,
        "winner": listing_info.winner
    })

@login_required
def my_listings(request):
    # Listings from the logged user
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(user=request.user),
        "listing_owner": request.user
    })



def search(request):
    if request.method == "POST":
        search_criteria = request.POST["search"]
        return render(request, "auctions/index.html", {
            #icontais is a case insentitive like query
            "listings": Listing.objects.filter(Q(title__icontains=search_criteria) | Q(description__icontains=search_criteria))
    })

@login_required
def add_watchlist(request, listing_id):
    listing_info = ListingInfo(request, listing_id)

    # If the user isn't watching the listing yet.
    if not listing_info.watch:
        WatchList.objects.create(user = request.user, listing = listing_info.listing)
        
    return render(request, "auctions/listing.html", {
        "listing": listing_info.listing,
        "category": listing_info.category,
        "comments": listing_info.comments, 
        "is_watching": True, 
        "is_owner": listing_info.is_owner
    })

@login_required
def remove_watchlist(request, listing_id):
    listing_info = ListingInfo(request, listing_id)
    if listing_info.watch:
        listing_info.watch.delete() 

    return render(request, "auctions/listing.html", {
        "listing": listing_info.listing,
        "category": listing_info.category,
        "comments": listing_info.comments, 
        "is_watching": False, 
        "is_owner": listing_info.is_owner
    })

@login_required
def bidding(request, listing_id):
    listing_info = ListingInfo(request, listing_id)
    if request.method == "POST":
        bid = request.POST["bid"]
        if (bid):
            listing_info.listing.price = float(bid)
            listing_info.listing.save()
            Bid.objects.create(user = request.user, price = bid, listing = listing_info.listing)

    return render(request, "auctions/listing.html", {
        "listing": listing_info.listing,
        "category": listing_info.category,
        "comments": listing_info.comments, 
        "is_watching": listing_info.watch, 
        "is_owner": listing_info.is_owner
    })

@login_required
def close_bidding(request, listing_id):
    listing_info = ListingInfo(request, listing_id)
    listing_info.listing.sold = True
    listing_info.listing.save()

    return HttpResponseRedirect(reverse('listing', kwargs={"listing_id": listing_id}))

def categories(request):  
    result = []
    categories_list = Category.objects.all()
 
    for c in categories_list:
        qtd = Listing.objects.filter(category=c).count() # quantity of listings in each category
        tupl = { "category": c,
                 "qtd": qtd,
               }
       
        result.append(tupl)

    return render(request, "auctions/categories.html", {
        "results": result
    })

@login_required
def by_category(request, category_id):

    category = Category.objects.get(pk = category_id)
    listings = Listing.objects.filter(category_id = category_id)

    return render(request, "auctions/index.html", {
        "from_category": category,
        "listings": listings
    })

@login_required
def watchlist(request):
    listing_ids = WatchList.objects.filter(user = request.user).values('listing')
    listing = Listing.objects.filter(id__in = listing_ids)
    return render(request, "auctions/watchlist.html", {
        "listings": listing
    })

@login_required
def remove_listing(request, listing_id):
    listing_info = ListingInfo(request, listing_id)
    if (listing_info.is_owner):
        listing_info.listing.remove()
    
    return index(request)