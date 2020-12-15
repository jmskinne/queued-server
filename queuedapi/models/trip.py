from django.db import models

class Trip(models.Model):
    """Trip model"""
    vacationer = models.ForeignKey("QueueUser", on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    hotel = models.CharField(max_length=150)
    date_start = models.DateField(auto_now=False)
    date_end = models.DateField(auto_now=False)
