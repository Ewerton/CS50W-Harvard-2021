from user.models.user import User
from django.db import models
from utils.functions import upload_to_path


class Photo(models.Model):

    photo = models.FileField(upload_to=upload_to_path, max_length=100)
    user = models.ForeignKey(User, related_name='photos', on_delete=models.CASCADE)

    @property
    def get_photo(self):
        return self.photo

    @property
    def get_user(self):
        return self.user

    class Meta:
        verbose_name = 'Photo'
        verbose_name_plural = 'Photos'
        ordering = ['id']
