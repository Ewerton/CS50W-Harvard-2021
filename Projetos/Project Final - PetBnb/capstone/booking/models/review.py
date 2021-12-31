from django.db import models
from user.models.profile_client import ProfileClient
from user.models.profile_server import ProfileServer


class Review(models.Model):
    booking = models.ForeignKey('Booking', on_delete=models.CASCADE, related_name='booking')
    profile_client_author = models.ForeignKey(ProfileClient, on_delete=models.CASCADE, related_name='profile_client_author')
    date = models.DateField()
    comment = models.TextField(blank=False, null=False, default='', max_length=1000)
    profile_server_reviewed = models.ForeignKey(ProfileServer, on_delete=models.CASCADE, related_name='profile_server_reviewed')
    rating = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'Author (Profile Client): {self.profile_client_author.get_name()}  |  User Reviewed (Profile Server): {self.profile_server_reviewed.get_name()}  | Rating: {self.rating}  Review: {self.comment[:10]}...' 