from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class gameCoordinates(models.Model):
    px = models.IntegerField(default=5)
    py = models.IntegerField(default=225)
    ox = models.IntegerField(default=730)
    oy = models.IntegerField(default=225)
    # bx = models.IntegerField(default=0)
    # by = models.IntegerField(default=0)

    class Meta:
        abstract = True