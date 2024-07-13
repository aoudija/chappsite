from django.db import models
from django.contrib.auth.models import User
from game.models import gameCoordinates


class Round(models.Model):#number of matches = number of participants - 1
    pass

class Match(models.Model):#will take two participants
    participant1 = models.ForeignKey(User)
    participant2 = models.ForeignKey(User)
    game: gameCoordinates = models.ForeignKey(gameCoordinates)
    typeOfMatch = models.CharField(max_length=2,default='rg')
    
# Create your models here.
class tournament(models.Model):
    participant = models.ManyToManyField(User)
    numberParticipants = models.IntegerField(default=4)

class base(models.model):
    pass

class x(base):
    pass