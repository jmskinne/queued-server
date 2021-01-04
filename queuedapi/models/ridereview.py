from django.db import models

class RideReview(models.Model):

    ride = models.ForeignKey("Ride", on_delete=models.CASCADE)
    reviewer = models.ForeignKey("QueueUser", on_delete=models.CASCADE)
    rating = models.IntegerField(null=True)
    review = models.TextField(null=True)

    

