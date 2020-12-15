from django.db import models

class RideReview(models.Model):

    ride_id = models.CharField(max_length=100)
    ride_name = models.CharField(max_length=200)
    reviewer = models.ForeignKey("QueueUser", on_delete=models.CASCADE)
    rating = models.IntegerField(null=True)
    review = models.TextField(null=True)

