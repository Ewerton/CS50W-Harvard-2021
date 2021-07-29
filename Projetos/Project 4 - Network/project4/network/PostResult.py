
from network.models import Preference

#represents a Post and the metadata associated to it
class PostResult():
    
    def __init__(self, post, liked):
        self.post = post
        self.liked = liked
   
