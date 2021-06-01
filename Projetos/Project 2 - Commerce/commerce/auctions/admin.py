from django.contrib import admin
#from django.contrib.auth import admin
# from django.contrib.auth.admin import UserAdmin
# Register your models here.
from .models import User, Listing, Bid, Comment, Category, WatchList

admin.site.register(User)
admin.site.register(Listing)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(WatchList)