from django.db import models
from django.utils import timezone
from Accounts_app.models import CustomUser
from Auction_app.models import AuctionDB


class Bid(models.Model):
    auction = models.ForeignKey(AuctionDB, on_delete=models.CASCADE, related_name="bids")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} bid ₹{self.amount} on {self.auction.title}"



