from django.db import models
from django.conf import settings

class QueueUser(models.Model):
    """ Representation of a rare user account that a user can create """
    profile_image_url = models.URLField()
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)