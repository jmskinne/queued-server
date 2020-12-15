from django.db import models

class RideFavorite(models.Model):
    ride_id = models.CharField(max_length=100)
    ride_name = models.CharField(max_length=200)
    vacationer = models.ForeignKey("QueueUser", on_delete=models.CASCADE)
    favorite = models.BooleanField(default=False)
