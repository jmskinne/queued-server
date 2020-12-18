from django.db import models

class Itinerary(models.Model):
    trip = models.ForeignKey("Trip", on_delete=models.CASCADE)
    park_date = models.DateTimeField()