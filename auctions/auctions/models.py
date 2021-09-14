from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model): 
    title = models.CharField(max_length=64)

    def __str__(self):
        return self.title


class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category,                                 
                                 on_delete=models.CASCADE,
                                 related_name='listing_category')
    img_url = models.URLField(max_length=250)
    created_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    winner = models.CharField(max_length=64, blank=True)

    def __str__(self):
        return (f"{self.title} - User: {self.user}")


class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return (f"Price: {self.price} - {self.listing.title} - User: {self.user}")

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    comment = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.listing.title} - {self.comment} - {self.user} - {self.timestamp} "

class WatchList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
