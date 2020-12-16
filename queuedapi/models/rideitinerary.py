from django.db import models

class RideItinerary(models.Model):
    itinerary = models.ForeignKey("Itinerary", on_delete=models.CASCADE)
    ride = models.ForeignKey("Ride", on_delete=models.CASCADE)
    order = models.IntegerField(null=True)