from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class StreamPlatform(models.Model):
    name = models.CharField(max_length=30)
    about = models.CharField(max_length=255)
    website = models.URLField(max_length=100)

    def __str__(self):
        return self.name + " " + str(self.id)
    

class WatchList(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    platform = models.ForeignKey(StreamPlatform, on_delete=models.CASCADE, related_name="watchlist")
    active = models.BooleanField(default=True)
    avg_rating = models.FloatField(default=0)
    number_rating = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title + " | " + self.platform.name
    

class Review(models.Model):
    review_user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=200, null=True)
    rating = models.PositiveBigIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    watchlist = models.ForeignKey(WatchList, on_delete=models.CASCADE, related_name="reviews")
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.review_user.username + " | " + self.watchlist.title + " | " + str(self.rating)
