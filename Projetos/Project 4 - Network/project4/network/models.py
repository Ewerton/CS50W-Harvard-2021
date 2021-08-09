from django.db import models
from django.utils import timezone
#from django.contrib.auth.models import User
from users.models import User
from django.urls import reverse

class Post(models.Model):
    content = models.TextField(max_length=1000)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    #likes= models.IntegerField(default=0)

    def __str__(self):
        return f'Post ID: {self.id}  |  Author: {self.author.username}  |  Content: {self.content[:10]}...' 

    @property
    def CommentsCount(self):
        return Comment.objects.filter(post=self).count()

    def LikedBy(self, user):
        return Preference.objects.filter(post_id=self.id, user_id=user.id, value=1).exists()
    
    @property
    def LikeCount(self):
        return Preference.objects.filter(post_id=self.id, value=1).count()

class Comment(models.Model):
    content = models.TextField(max_length=150)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class Preference(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    post= models.ForeignKey(Post, on_delete=models.CASCADE)
    value= models.IntegerField() #1 = Like | 2 = Dislike 
    date= models.DateTimeField(auto_now= True)

    def __str__(self):
        return str(self.user) + ':' + str(self.post) +':' + str(self.value)

    class Meta:
       unique_together = ("user", "post", "value")
