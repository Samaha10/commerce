from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass



class Listing(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=19, decimal_places=2)
    #image = models.ImageField(blank=True, null=True,upload_to='uploads/')
    image = models.URLField(max_length=200, blank=True, null=True)

    cat_choices = [
        ('Fashion', 'Fashion'),
        ('Toys', 'Toys'),
        ('Electronics', 'Electronics'),
        ('Home', 'Home'),
    ]
    category = models.CharField(choices=cat_choices, max_length=50, blank=True, null=True)
    watchlist = models.ManyToManyField(User, related_name="watchlist")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner", null=True)
    closed = models.BooleanField(default=False)
    #highest = models.ForeignKey(User, blank=True, null=True)
       

class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=19, decimal_places=2)

class Comment(models.Model):
    tweet = models.TextField()
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

