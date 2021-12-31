from django.contrib import admin

from .models.photo import Photo
from .forms.photo import PhotoModelForm


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    form = PhotoModelForm
    list_display = (
        'id',
        'photo',
        'user',
    )
