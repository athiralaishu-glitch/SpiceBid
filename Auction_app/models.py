from django.db import models
from django.utils import timezone
from Accounts_app.models import *

# Create your models here.

class AuctionDB(models.Model):
    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    starting_price = models.DecimalField(max_digits=10, decimal_places=2)
    ended_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    image = models.ImageField(upload_to='auction_items/', blank=True, null=True)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    @property
    def is_live(self):
        now = timezone.localtime(timezone.now())
        return self.is_active and self.start_time <= now <= self.end_time