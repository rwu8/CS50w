from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    # (e.g. Fashion, Toys, Electronics, Home, etc.)
    category = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.category}"

class Auction(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=500)
    starting_price = models.DecimalField(max_digits=10, decimal_places=2) 
    current_price = models.DecimalField(default=None, null=True, max_digits=10, decimal_places=2)
    current_price_user = models.ForeignKey(User, null=True, default=None, on_delete=models.CASCADE, related_name="filter_bidding_user")
    photo = models.TextField(null=True, default=None, max_length=500)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,)
    listing_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="filter_listing_user")
    winning_user = models.ForeignKey(User, null=True, default=None, on_delete=models.CASCADE, related_name="filter_winning_user")
    created = models.DateField(auto_now=False, auto_now_add=True)
    is_closed = models.BooleanField()

class Comment(models.Model):
    comment = models.TextField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="filter_comment_user")
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="filter_comment_auction")
    created = models.DateField(auto_now=False, auto_now_add=True)

class WatchList(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="filter_watchlist_auction")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="filter_watchlist_user")