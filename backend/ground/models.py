from django.db import models

# Create your models here.
class Player(models.Model):
    nickname = models.CharField(max_length=20, unique=True)

class Game(models.Model):
    # Player1 = Player.ForeignKey
    # Player2 = Player.ForeighKey
    # Gamestate somehow. Nine variables? Sq00, Sq01, s02, Sq10, Sq11 ...
    pass

