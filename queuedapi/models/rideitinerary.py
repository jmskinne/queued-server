from django.db import models

class RideItinerary(models.Model):
    itinerary = models.ForeignKey("Itinerary", on_delete=models.CASCADE)
    ride_id = models.CharField(max_length=100)
    name = models.CharField(max_length=200)
    order = models.IntegerField(null=True)