from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class gameCoordinates(models.Model):
    player = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    opponent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    px = models.IntegerField(default=5)
    py = models.IntegerField(default=225)
    ox = models.IntegerField(default=730)
    oy = models.IntegerField(default=225)
    # bx = models.IntegerField(default=0)
    # by = models.IntegerField(default=0)
    # scorePlayer = models.IntegerField(default=0)
    # scoreOpponent = models.IntegerField(default=0)
    # finished = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.player.username} vs {self.opponent.username}"