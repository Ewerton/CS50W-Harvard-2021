
from auctions.models import Bid, Category, Comment, Listing, WatchList


class ListingInfo():
    """Describes a listing in the context of an request."""
    def __init__(self, request, listing_id):
        self.request = request
        self.listing_id = listing_id
        self.listing = Listing.objects.get(id=listing_id)
        self.user = request.user
        self.is_owner = True if self.listing.user == self.user else False
        self.category = Category.objects.get(category=self.listing.category)
        self.comments = Comment.objects.filter(listing=self.listing.id)
        self.watch = None
        self.is_watching = False
        if request.user.is_authenticated:
            self.watch = WatchList.objects.filter(user = self.user, listing = self.listing)
            self.is_watching = len(self.watch) > 0 

        self.winner = None
        # If the item is sold, gets the highest bid for ths listing
        if self.listing.sold:
            highest_bid = Bid.objects.filter(listing = self.listing).order_by('price').last() 
            self.winner = highest_bid.user # the user who made the highest bid

    # def add_comment(comment):
    #     pass

    # def remove_comment(comment):
    #     pass

    # def add_watchlist(user):
    #     pass

    # def remove_watchlist(user):
    #     pass

    # def am_i_whatching():
    #     pass

    # def am_i_owner():
    #     pass
    