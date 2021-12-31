from django.db import models
from .user import User
from photo.models.photo import Photo


class ProfileClient(models.Model):
    name = models.CharField(blank=False, null=False, max_length=200)
    user = models.ForeignKey(User, related_name='profile_client', on_delete=models.CASCADE)
    pet_photo = models.CharField(max_length=500, default='')

    @property
    def get_name(self):
        return self.name

    @property
    def get_user(self):
        return self.user

    @staticmethod
    def to_list(__str):
        return str(__str).replace('[', '').replace("'", '').replace(' ', '').replace(']', '').split(',')

    @property
    def get_pet_photo(self):
        return self.pet_photo

    @property
    def get_url_pet_photo(self):
        return Photo.objects.get(id=int(self.to_list(self.pet_photo)[0])).get_photo

    @property
    def get_url_list_pet_photo(self):
        return [(i.id, i.get_photo) for i in Photo.objects.filter(id__in=self.to_list(self.pet_photo))]

    class Meta:
        verbose_name = 'Client Profile'
        verbose_name_plural = 'Client Profiles'
        ordering = ['id']
