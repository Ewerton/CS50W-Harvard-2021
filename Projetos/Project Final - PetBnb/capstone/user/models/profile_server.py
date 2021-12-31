from django.db import models
from .user import User
from pet_type.models.pet_type import PetType
from photo.models.photo import Photo


class ProfileServer(models.Model):
    name = models.CharField(blank=False, null=False, max_length=200)
    description = models.TextField(blank=False, null=False, default='')
    user = models.ForeignKey(User, related_name='profile_server', on_delete=models.CASCADE)
    latitude = models.DecimalField(max_digits=22, decimal_places=16)
    longitude = models.DecimalField(max_digits=22, decimal_places=16)
    pet_type = models.CharField(max_length=100)
    local_photos = models.CharField(max_length=500)

    @property
    def get_name(self):
        return self.name

    @property
    def get_description(self):
        return self.description

    @property
    def get_user(self):
        return self.user

    @property
    def get_latitude(self):
        return self.latitude

    @property
    def get_longitude(self):
        return self.longitude

    @staticmethod
    def to_list(__str):
        return str(__str).replace('[', '').replace("'", '').replace(' ', '').replace(']', '').split(',')

    @property
    def get_pet_type(self):
        __pet_type = str()
        for i in self.to_list(self.pet_type):
            try:
                if len(__pet_type) == 0:
                    __pet_type = PetType.objects.get(id=(int(i))).get_type
                else:
                    __pet_type = __pet_type + ', ' + PetType.objects.get(id=(int(i))).get_type
            except:
                pass
        return str(__pet_type)

    @property
    def get_local_photos(self):
        return self.local_photos

    @property
    def get_url_local_photos(self):
        if len(str(self.local_photos)) >> 0:
            return Photo.objects.filter(id__in=self.to_list(self.local_photos))
        return Photo.objects.none()

    @property
    def get_location_cover_photo(self):
        return Photo.objects.get(id=int(self.to_list(self.local_photos)[0])).get_photo

    class Meta:
        verbose_name = 'Server Profile'
        verbose_name_plural = 'Server Profiles'
        ordering = ['id']
