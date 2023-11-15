from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django import forms
from .models import Player
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache
from django.urls import reverse
import datetime

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


def arena(request):
    """Opens the arena proper. Renders list of those who are online and not online."""
    players_online = cache.get("last_seen_online")
    all_players = list(Player.objects.all())
    # go through players_online, remove those instances from players offline
    players_offline = []
    for player in all_players:
        for player_online in players_online:
            if (player.nickname != player_online):
                players_offline.append(player.nickname)          
    return render(request, "ground/arena.html", {
        "players_online":players_online,
        "players_offline":players_offline,
        "nickname":request.session["Nickname"],
        "buttonForm":buttonForm(),
    })

def tictactoe(request, **kwargs):
    # return render(request,"ground/tictactoe.html", {
    #     "message":"I will implement tic-tac-toe here",
    # })
    return render(request, "ground/tictactoe.html", {
        "message": "I will implement tictactoe."
    })
