
#from network.models import Preference

#represents a Post and the metadata associated to it
class FollowResult():
    
    def __init__(self, user, follow_you, do_you_follow):
        self.user = user
        self.follow_you = follow_you
        self.do_you_follow = do_you_follow
   
