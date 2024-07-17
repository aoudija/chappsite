from django.db import models
from django.contrib.auth.models import User
from game.models import gameCoordinates

    
# Create your models here.
class Tournament(models.Model):
    participant = models.ManyToManyField(User)
    numberParticipants = models.IntegerField(default=4)
    round = models.IntegerField(default=1)
    
    def next_round(self):
        matches = Match.objects.filter(finished=False, )
        winners = [match.winner for match in matches]
        for i in range(0, len(winners), 2):
            if i + 1 < len(winners):
                new_match = Match.objects.create(player=winners[i], opponent=winners[i+1],
                                     typeOfMatch='tr', round=self.round+1)
                new_match.save()
        self.round += 1

    def is_complete(self):
        return self.round == self.numberParticipants - 1

class Match(gameCoordinates):#will take two participants
    player = models.ForeignKey(User)
    opponent = models.ForeignKey(User)
    typeOfMatch = models.CharField(max_length=2,default='rg')
    winner = models.ForeignKey(User)
    round = models.IntegerField(default=1)
    scorePlayer = models.IntegerField(default=0)
    scoreOpponent = models.IntegerField(default=0)
    finished = models.BooleanField(default=False)
    tournament = models.ForeignKey(Tournament, )