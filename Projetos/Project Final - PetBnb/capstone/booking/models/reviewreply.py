from django.db import models
from user.models.profile_client import ProfileClient
from user.models.profile_server import ProfileServer
from booking.models.review import Review

class ReviewReply(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='review')
    date = models.DateField()
    comment = models.TextField(blank=False, null=False, default='', max_length=1000)

    #def __str__(self):
    #    return f'Author (Profile Client): {self.profile_client_author.get_name()}  |  User Reviewed (Profile Server): {self.profile_server_reviewed.get_name()}  | Rating: {self.rating}  Review: {self.comment[:10]}...' 