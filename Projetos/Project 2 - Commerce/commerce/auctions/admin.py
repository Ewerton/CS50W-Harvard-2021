from django.contrib import admin
#from django.contrib.auth import admin
# Register your models here.
from .models import User, Listing, Bid, Comment, Category, WatchList

admin.register(User)
admin.register(Listing)
admin.register(Bid)
admin.register(Comment)
admin.register(Category)
admin.register(WatchList)