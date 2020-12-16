from django.db import models

class Ride(models.Model):
    ride = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=200)
    lat = models.DecimalField(max_digits=15, decimal_places=10)
    longitude = models.DecimalField(max_digits=15, decimal_places=10)