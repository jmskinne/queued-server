from django.db import models

class RideFavorite(models.Model):
    ride = models.ForeignKey("Ride", on_delete=models.CASCADE)
    vacationer = models.ForeignKey("QueueUser", on_delete=models.CASCADE)
    favorite = models.BooleanField(default=False)
