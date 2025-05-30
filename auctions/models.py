from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

class User(AbstractUser):
    pass

class Category(models.Model):
    categoryName= models.CharField(max_length=50)
    
    def __str__(self):
        return self.categoryName

class Bid(models.Model):
    bid = models.IntegerField(
        
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    

    class Meta:
        ordering = ['-bid']

class Listing(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    imageUrl = models.URLField(max_length=1000, blank=True,  default="http://127.0.0.1:8000/static/images/default.png")
    price = models.ForeignKey(Bid, on_delete=models.CASCADE, blank=True, null=True, related_name="bidPrice")
    isActive = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user")
    category = models.ForeignKey(Category,on_delete=models.CASCADE,blank=True,null=True, related_name="category")
    watchList = models.ManyToManyField(User, related_name="listingWatchlist", blank=True)
    
    def __str__(self):
        return self.title

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="userComment")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, null=True, related_name="listingComment")
    message = models.CharField(max_length=200)

    def __str__ (self):
        return f"{self.author}" f"{self.listing}"



