from django.contrib import admin
from .models.booking import Booking
from .models.review import Review
from .models.reviewreply import ReviewReply

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin): 
    list_display = (
        'id', 
        'profile_client_author', 
        'date', 
        'comment', 
        'profile_server_reviewed', 
        'rating', 
        )

@admin.register(ReviewReply)
class ReviewAdmin(admin.ModelAdmin): 
    list_display = (
        'id', 
        'review', 
        'date', 
        'comment', 
        )

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'status',
        'profile_client',
        'profile_server',
        'date_of_interest',
        'confirmed',
        'pet_photo',
        'pet_description',
        'decision',
    )
