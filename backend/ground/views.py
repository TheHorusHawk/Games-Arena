from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django import forms
from .models import Player, Game, TicTacToeMatrix
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache
from django.urls import reverse
import datetime
import json

from django import forms

# Create your views here.

#API
def toggle_in(request):
    """Will activate middleware and put the player in"""
    return HttpResponseRedirect(reverse("arena"))

#FORMS
class buttonForm(forms.Form):
    pass


class newPlayer(forms.Form):
    body = forms.CharField(label = "Nickname",widget=forms.TextInput(attrs={'maxlength':'20','autofocus':'autofocus'}))

#Helper Functions

def put_online(nickname):
    """Helper function receives nickname and adds it to cached online list with timestamp of now"""
    seen_online = cache.get("last_seen_online")
    seen_online[nickname]=datetime.datetime.now()
    cache.set("last_seen_online", seen_online, None)


def index(request):
    """Welcome screen. Checks or creates Nickname in session and redirects to the arena."""
    #Comment out once working
    #request.session.flush()
    if request.session.get("Nickname", False):
            """If there's a nickname load arena"""
            return arena(request)
    if request.method == "POST":
        form = newPlayer(request.POST)
        if form.is_valid():
            form=form.cleaned_data
            submitted_nickname=form["body"]
            try:
                Player(nickname=submitted_nickname).save()
            except IntegrityError:
                return render(request, "ground/index.html",{
                            "message":"Nickname already taken, please try again.",
                            "playerForm":newPlayer()                  
                 })
            #save nickname in session
            request.session['Nickname'] = submitted_nickname
            #add nickname to is_online list
            put_online(submitted_nickname)
            return arena(request)
        else:
            return render(request, "ground/index.html",{
                            "message":"Something went wrong, please try again.",
                            "playerForm":newPlayer()                  
                 }) 
    return render(request, "ground/index.html",{
                  "playerForm":newPlayer()                  
    })


def arena(request, *message):
    """Opens the arena proper. Renders list of those who are online and not online."""
    players_online = cache.get("last_seen_online")
    all_players = list(Player.objects.all())
    # go through players_online, remove those instances from players offline
    players_offline = []
    #Puts a message in the message variable, empty string if none is supplied
    if message:
        message=message[0]
    else:
        message=""
    for player in all_players:
        for player_online in players_online:
            if (player.nickname != player_online):
                players_offline.append(player.nickname)          
    return render(request, "ground/arena.html", {
        "message": message,
        "players_online":players_online,
        "players_offline":players_offline,
        "nickname":request.session["Nickname"],
        "buttonForm":buttonForm(),
    })

def tictactoe(request, **kwargs):
    #Try/catch?Gets players from database - if they exist if not back to arena
    try:
        player1 = Player.objects.get(nickname=kwargs['Player1'])
        player2 = Player.objects.get(nickname=kwargs['Player2'])
    except:
        message = "Can't start Tic Tac Toe game, players don't seem to exist"
        return arena (request, message)
    
    #Checks if game exists
    try:
        thisGame = Game.objects.get(player1=player1, player2=player2)
    except:
        #if not make new one
        board = TicTacToeMatrix()
        board.save()
        newGame = Game(player1=player1, player2=player2, board=board, activePlayer=player1)     
        newGame.save()
        thisGame = newGame
    
    if request.method == "POST":
        """Implements making a move or restarting game"""
        #IF request.session.nickname == thisGame.activePlayer
        #loads which square information from request
        square = json.loads(request.body)['id']
        if square == 'Restart':
            thisGame.delete()
            board = TicTacToeMatrix()
            board.save()
            newGame = Game(player1=player1, player2=player2,board=board, activePlayer=player1)
            newGame.save()
            thisGame = newGame
        else:
            isPlayer1 = thisGame.activePlayer == thisGame.player1
            # set correct integer to record play (1 for player 1, 2 for player 2)
            integer = ((2, 1)[isPlayer1])
            setattr(thisGame.board, square, integer)
            thisGame.board.save()
            # changes active player
            newActivePlayer = ((thisGame.player1, thisGame.player2)[isPlayer1])
            thisGame.activePlayer = newActivePlayer
            thisGame.save()

    board = thisGame.board

    activePlayer=thisGame.activePlayer
    toPlay = request.session["Nickname"] == activePlayer.nickname
    
    room_name = f"{player1.nickname}{player2.nickname}"
    message = "I am implementing tictactoe."
    
    over = checkOver(thisGame)
    #changes what is fed based on whether game is over
    if (over[0]):
        if over[1]=="draw":
            message=f"Game over. It's a draw."
        if over[1]=="player1":
            message = f"Game over. {player1.nickname} won."
        if over[1] == "player2":
            message = f"Game over. {player2.nickname} won."
        activePlayer.nickname = 'None'
        toPlay = False


    return render(request, "ground/tictactoe.html", {
        "message": message,
        "activePlayer": activePlayer.nickname,
        "game":thisGame,
        "board":board,
        "toPlay":toPlay,
        "room_name": room_name,
        "over":over,
    })

#Checks if the game is over
def checkOver(game):
    board = game.board
    sum = sumAll(board)
    #If 5 moves haven't been made, game can't be over
    if sum < 7:
        return (False,)
    #Checks for win on each line/diagonal
    win = checkwin(board.sq00, board.sq01, board.sq02)
    if win[0]:
        return win
    win = checkwin(board.sq10, board.sq11, board.sq12)
    if win[0]:
        return win
    win = checkwin(board.sq20, board.sq21, board.sq22)
    if win[0]:
        return win
    win = checkwin(board.sq00, board.sq10, board.sq20)
    if win[0]:
        return win
    win = checkwin(board.sq01, board.sq11, board.sq21)
    if win[0]:
        return win
    win = checkwin(board.sq02, board.sq12, board.sq22)
    if win[0]:
        return win
    win = checkwin(board.sq00, board.sq11, board.sq22)
    if win[0]:
        return win
    win = checkwin(board.sq02, board.sq11, board.sq20)
    if win[0]:
        return win
    #Checks if all the squares have been filled
    if sum == 13:
        return (True, "draw")
    return (False,)


def sumAll(board):
    return board.sq00+board.sq01+board.sq02+board.sq10+board.sq11+board.sq12+board.sq20+board.sq21+board.sq22

def checkwin(a,b,c):
    #If any square in line has not been filled can't be a win
    if a==0 or b==0 or c==0:
        return (False,)
    #If it's three ones, player 1 wins
    elif a+b+c == 3:
        return (True, "player1")
    #If it's three twos, player 2 wins
    elif a+b+c == 6:
        return (True, "player2")
    else:
        return (False,)


# TICTACTOE object:
#     var playertomove
#     init (if Game between these two not exist)
#     newGame = Game(player1=Player(nickname=kwargs['Player1']), player2=Player(
#         nickname=kwargs['Player2']))
#     var playertomove = Player1

#     run:
#         render, etc.
    # makemove - change sqxx with playercurrentlyplaying namesymbol. 
    # Make sure request comes from him.
    
