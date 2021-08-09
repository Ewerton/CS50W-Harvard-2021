#from network.models import Post
#from network.models import Post
from django.db import models
#from django.contrib.auth.models import User
from PIL import Image
from django.apps import apps
from django.conf import settings as project_settings

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    #contact = models.CharField(max_length=20, blank=True)#id = models.AutoField(primary_key=True)
    pass

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic_folder = project_settings.PROFILE_PICS_URL 
    image = models.ImageField(default=profile_pic_folder + '/default.png', upload_to=profile_pic_folder, max_length=500)

    def __str__(self):
        return f'{self.user.username} Profile'

    @property
    def followers_count(self):
        return Follow.objects.filter(follow_user=self.user).count()

    @property
    def following_count(self):
        return Follow.objects.filter(user=self.user).count()


    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save()

        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Follow(models.Model):
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    follow_user = models.ForeignKey(User, related_name='follow_user', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

