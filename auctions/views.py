from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User,Category, Listing, Comment, Bid

def listing(request, id):
    listingData = Listing.objects.get(pk=id)
    isListingInWatchList = request.user in listingData.watchList.all() # You can add real logic here later
    allComments =Comment.objects.filter(listing=listingData)
    return render(request, "auctions/listing.html", {
        "listing": listingData,
        "isListingInWatchList": isListingInWatchList,
        "allComments": allComments
    })

def displayWatchList(request):
    currentUser = request.user 
    listings = currentUser.listingWatchlist.all({
        "listings": listings 
    })

    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })

def removeWatchList(request, id):
    listingData = Listing.objects.get(pk=id)
    currentUser = request.user
    listingData.watchList.remove(currentUser)
    return HttpResponseRedirect(reverse("listing", args=(id, )))

def addWatchList(request,id):
    if request.method == "POST":
        listingData = Listing.objects.get(pk=id)
        currentUser = request.user
        listingData.watchList.add(currentUser)
        return HttpResponseRedirect(reverse("listing", args=(id, )))
    return redirect("listing", id=id)

def index(request):
    activeListing = Listing.objects.filter(isActive=True)
    allCategories = Category.objects.all()
    return render(request, "auctions/index.html",{
        "listings": activeListing,
        "categories": allCategories,
    })

def addComment(request,id):
    currentUser = request.user 
    listingData = Listing.objects.get(pk=id)
    message = request.POST["newComment"]

    if message:
        newComment = Comment(
            author=currentUser,
            listing=listingData,
            message=message
        )

        newComment.save()
    
        return HttpResponseRedirect(reverse("listing", args=(id,)))
    else:
        return HttpResponseRedirect(reverse("listing", args=(id,)))

    

def displayCategory(request):
    if request.method == "POST":
        categoryFromForm = request.POST['category']
        category = Category.objects.get(categoryName=categoryFromForm)
        activeListing = Listing.objects.filter(isActive=True, category=category)

        allCategories = Category.objects.all()
        return render(request, "auctions/index.html",{
            "listings": activeListing,
            "categories": allCategories,

        })

def createListing(request):
    if request.method == "GET":
        allCategories = Category.objects.all()
        return render(request,"auctions/create.html",{
            "categories": allCategories
        })

    else:
        # get data from the form 
        title = request.POST["title"]
        description = request.POST["description"]
        imageurl = request.POST.get("imageurl",None)

        price = request.POST["price"]
        
        category = request.POST["category"]

         # Optional: Check if image was uploaded
        if imageurl is None:
            print("No image uploaded")
        #who is the user
        currentUser = request.user

        # get all content about the category
        categoryData = Category.objects.get(categoryName=category)

        # Create  a Bid Object
        bid = Bid(bid=float(price), user=currentUser)

        bid.save()

    
        # create a new listing
        newListing = Listing(
            title=title,
            description=description,
            imageUrl=imageurl,
            price=bid,
            
            category=categoryData,
            owner=currentUser

        
        )
        #insert item into database
        newListing.save()

        #redirect to index
        return HttpResponseRedirect(reverse(index))



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
