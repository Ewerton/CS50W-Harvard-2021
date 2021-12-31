from django.contrib import admin

from .models.availability import Availability


@admin.register(Availability)
class AvailabilityAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'profile',
        'date',
    )
