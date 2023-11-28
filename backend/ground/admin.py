from django.contrib import admin

# Register your models here.
from .models import Player, TicTacToeMatrix, Game
admin.site.register(Player)
admin.site.register(TicTacToeMatrix)
admin.site.register(Game)
