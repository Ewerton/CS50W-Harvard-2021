from django.contrib.auth.models import AbstractUser
from django.db import models
from django.http import HttpResponse

class User(AbstractUser):
    contact = models.CharField(max_length=20, blank=True)#id = models.AutoField(primary_key=True)
    #pass


class Category(models.Model):
    category = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.category}"


class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    title = models.CharField(max_length=64)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.ForeignKey(Category, default=None, blank=True, null=True, on_delete=models.CASCADE, related_name="listing_category")
    categories = models.ManyToManyField(Category, default=None, blank=True, null=True, related_name="listing_categories") 
    image_url = models.URLField(max_length=400, default="/auctions/static/images/no_proto.png", blank=True, null=True)
    sold = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} posted by {self.user} Initial Price: {self.price}"
   
class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    
    def __str__(self):
        return f"Bid on item: {self.listing}. User: {self.user}. Price: {self.price}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    comment = models.TextField()
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.comment} - {self.user}"


class WatchList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)