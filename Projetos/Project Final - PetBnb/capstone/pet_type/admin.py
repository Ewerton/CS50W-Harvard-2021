from django.contrib import admin


from .models.pet_type import PetType


@admin.register(PetType)
class PetTypeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'pet_type',
    )
