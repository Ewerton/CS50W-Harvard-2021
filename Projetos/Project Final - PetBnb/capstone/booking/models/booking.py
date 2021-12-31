from django.db import models
from user.models.profile_client import ProfileClient
from user.models.profile_server import ProfileServer
from photo.models.photo import Photo


class Booking(models.Model):
    profile_client = models.ForeignKey(ProfileClient, related_name='booking', on_delete=models.CASCADE)
    profile_server = models.ForeignKey(ProfileServer, related_name='booking', on_delete=models.CASCADE)
    date_of_interest = models.DateField()
    """
    confirmed = 0 - waiting confirmation
    confirmed = 1 - confirmed
    confirmed = 2 - refused
    """
    confirmed = models.PositiveIntegerField(default=0)
    pet_photo = models.CharField(max_length=500, default='')
    pet_description = models.TextField(blank=False, null=False, default='')
    decision = models.TextField(blank=False, null=False, default='')
    """
    status = 0 - A Booking was created, show notification to the server
    status = 1 - The server viewed the notification
    status = 2 - The server answered the request, show a notification to the client
    status = 3 - the client viewed the notification
    """
    status = models.PositiveIntegerField(default=0)

    @property
    def get_confirmed(self):
        return self.confirmed

    @property
    def get_decision(self):
        return self.decision

    @property
    def get_date_of_interest(self):
        return self.date_of_interest

    @property
    def get_profile_client(self):
        return self.profile_client

    @property
    def get_profile_server(self):
        return self.profile_server

    @staticmethod
    def to_list(__str):
        return str(__str).replace('[', '').replace("'", '').replace(' ', '').replace(']', '').split(',')

    @property
    def get_url_pet_photo(self):
        if len(str(self.pet_photo)) >> 0:
            return Photo.objects.filter(id__in=self.to_list(self.pet_photo))
        return Photo.objects.none()

    class Meta:
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'
        ordering = ['id']
