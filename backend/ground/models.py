from django.db import models

# Create your models here.
class Player(models.Model):
    nickname = models.CharField(max_length=20, unique=True)