from django.db import models

# Create your models here.
class Player(models.Model):
    nickname = models.CharField(max_length=20, unique=True)

class TicTacToeMatrix(models.Model):
    sq00 = models.PositiveSmallIntegerField(default=0)
    sq01 = models.PositiveSmallIntegerField(default=0)
    sq02 = models.PositiveSmallIntegerField(default=0)
    sq10 = models.PositiveSmallIntegerField(default=0)
    sq11 = models.PositiveSmallIntegerField(default=0)
    sq12 = models.PositiveSmallIntegerField(default=0)
    sq20 = models.PositiveSmallIntegerField(default=0)
    sq21 = models.PositiveSmallIntegerField(default=0)
    sq22 = models.PositiveSmallIntegerField(default=0)

class Game(models.Model):
    player1 = models.ForeignKey(
        Player, on_delete=models.CASCADE, related_name="player1")
    player2 = models.ForeignKey(
        Player, on_delete=models.CASCADE, related_name="player2")
    board = models.OneToOneField(TicTacToeMatrix, on_delete=models.CASCADE, related_name="board")