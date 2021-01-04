from django.db import models
from .ridereview import RideReview

class Ride(models.Model):
    ride = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=200)
    lat = models.DecimalField(max_digits=15, decimal_places=10)
    longitude = models.DecimalField(max_digits=15, decimal_places=10)


    @property
    def average_rating(self):
        ratings = RideReview.objects.filter(ride=self)
        total_rating = 0
        for rating in ratings:
            total_rating += rating.rating
        try:
            avg = total_rating / len(ratings)
            return avg
        except ZeroDivisionError:
            pass