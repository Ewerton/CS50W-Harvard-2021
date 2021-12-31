from django.db import models
from user.models.profile_server import ProfileServer


class Availability(models.Model):

    profile = models.ForeignKey(ProfileServer, related_name='availability', on_delete=models.CASCADE)
    date = models.DateField()

    @property
    def get_profile(self):
        return self.profile

    @property
    def get_date(self):
        return self.date

    class Meta:
        verbose_name = 'Availability'
        verbose_name_plural = 'Availabilities'
        ordering = ['id']
