from user.models.profile_client import ProfileClient
from django.db.models.signals import post_save
from user.models import User
from django.dispatch import receiver



# signal that gets fired after the user is saved
@receiver(post_save, sender=User)
def create_client_profile(sender, instance, created, **kwargs):
     if created:
        ProfileClient.objects.create(user=instance, name=instance.email)
