
from users.models import Follow
from network.models import Post

#represents a User and its associated data
class UserData():
    
    def __init__(self, user):
        self.user = user

    @property
    def post_count(self):
        return Post.objects.filter(author=self.user).count()
   
    @property
    def following_count(self):
        return self.user.following.count()

    @property
    def followers_count(self):
        return self.user.followers.count()

    @property
    def can_user_follow(self, user):
        return Follow.objects.filter(user=self.user, follow_user=user).count() == 0
