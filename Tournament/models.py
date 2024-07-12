from django.db import models
from django.contrib.auth.models import User


class Round(models.Model):#number of matches = number of participants - 1
    pass

class Match(models.Model):#will take two participants
    def __init__(self):
        pass
    participant1 = models.ForeignKey(User)
    participant2 = models.ForeignKey(User)

# Create your models here.
class tournament(models.Model):
    participant = models.ManyToManyField(User)
    NUMBERPARTICIPANTS_CHOICES = (
        (4, '4 participants'),
        (8, '8 participants'),
        )
    numberParticipants = models.IntegerField(choices=NUMBERPARTICIPANTS_CHOICES)
