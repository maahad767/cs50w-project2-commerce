from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass 


class Category(models.Model):
    name = models.CharField(max_length=64)
    
    def __str__(self):
        return f"{self.pk}: {self.name}"
        
    
class Listing(models.Model):
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL, related_name="listings")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    title = models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True)
    image_url = models.URLField(null=True, blank=True)
    minimum_bid_amount = models.DecimalField(decimal_places=2, max_digits=20)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.pk}: {self.title}"    


class Watchlist(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name="watchlist")
    listings = models.ManyToManyField(Listing)

    def __str__(self):
        return f"{self.owner}'s watchlist"
    


class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    amount = models.DecimalField(decimal_places=2, max_digits=20)
    is_winner = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.bidder} bidded {self.amount} for {self.listing.title}"
    

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    body = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user}: {self.body[:30]}"
    