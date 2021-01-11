from django.db import models

class HistoricalWait(models.Model):
    ride = models.CharField(max_length=100)
    wait = models.IntegerField(null=True)
    created_on = models.DateTimeField(auto_now_add=True)