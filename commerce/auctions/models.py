from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    type = models.CharField(max_length=64)

    def __str__(self):
        return self.type


class Listings(models.Model):
    title = models.CharField(max_length=64)
    seller_name = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="seller")
    image = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    startingPrice = models.FloatField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True, related_name="category")
    date = models.DateTimeField(auto_now_add=True)
    currentPrice = models.FloatField(blank=True, null=True)
    watchlisters = models.ManyToManyField(User, blank=True, related_name="watchlist")
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Bids(models.Model):
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="bids")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="bidder")
    offer = models.FloatField()

    def __str__(self):
        return f"{self.offer}"


class Comments(models.Model):
    title = models.ForeignKey(Listings, on_delete=models.CASCADE, blank=True, null=True, related_name="title_commented")
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="commenter")
    content = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f" {self.title.id} {self.commenter} commented on {self.title}: {self.content}"
