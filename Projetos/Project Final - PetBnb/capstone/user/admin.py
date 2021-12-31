from django.contrib import admin
from django.contrib.auth.models import Group
from .models.user import User
from .models.profile_server import ProfileServer
from .models.profile_client import ProfileClient
from .forms.user_create_form import UserCreateForm
# from .forms.profile_server import ProfileServerModelForm


@admin.register(ProfileClient)
class ProfileClientAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'user',
        'pet_photo'
    )


@admin.register(ProfileServer)
class ProfileServerAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'user',
        'description',
        'pet_type',
        'local_photos',
        'latitude',
        'longitude'
    )


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    form = UserCreateForm
    list_display = (
        'id',
        'email',
        'photo',
    )


admin.site.unregister(Group)
