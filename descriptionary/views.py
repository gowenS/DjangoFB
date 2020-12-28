from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from FreshBeignet.commonFunc import generateGameName
from .models import Game
import os, binascii, glob

refreshState = {}

def home(request):
    if 'gameName' in request.session: del request.session['gameName']
    if 'playerStack' in request.session: del request.session['playerStack']
    return render(request, "index.html")

# =============================== #
# ====== Host Client Views ====== #
# =============================== #
def host(request):
    if 'gameName' not in request.session:
        gameName = generateGameName()
        allGames = Game.objects.all()
        while allGames.filter(game_name=gameName).exists():
            gameName = generateGameName()
        game = Game()
        game.game_name = gameName
        game.tot_players = 0
        game.game_state = 0
        game.save()
        request.session['gameName'] = gameName
    else:
        gameName = request.session['gameName']
        game = Game.objects.get(game_name=gameName)
    context = {
        "game": game
    }
    request.session['gameState'] = getGameState(gameName)
    return render(request, "host.html", context)

def host_start(request):
    gameName = request.session['gameName']
    game = Game.objects.get(game_name=gameName)
    game.game_state = 1
    game.save()
    incrementGameState(gameName, request)
    return redirect('gameview')

def gameview(request):
    gameName = request.session['gameName']
    game = Game.objects.get(game_name=gameName)
    if game.game_state > game.player_list_set.count():
        request.session['playerStack'] = 1
        return redirect('showplayerstacks')
    all_submitted = True
    for plyr in game.player_list_set.all():
        if plyr.submit_state != game.game_state:
            all_submitted = False
    if all_submitted:
        game.game_state = game.game_state + 1
        game.save()
        incrementGameState(gameName,request)
        return redirect('gameview')
    context = {
        "game": game
    }
    request.session['gameState'] = getGameState(gameName)
    return render(request, "gameview.html", context)

def showplayerstacks(request):
    gameName = request.session['gameName']
    game = Game.objects.get(game_name=gameName)
    if request.method == 'POST':
        request.session['playerStack'] += 1
        return redirect('showplayerstacks')
    player= game.player_list_set.get(player_id=request.session['playerStack'])
    stack = getPlayerStack(game, player)
    context = {
        "game" : game,
        "player" : player,
        "stack" : stack
    }
    return render(request, "showplayerstacks.html", context)

# =============================== #
# ===== Player Client Views ===== #
# =============================== #
def join(request):
    if request.method == 'GET':
        return render(request, "join.html", {"join_error":''})
    if request.method == 'POST':
        gameName = str(request.POST.get('gameName')).upper()
        playerName = request.POST.get('playerName')
        join_error = ''
        if Game.objects.all().filter(game_name = gameName).exists():
            game = Game.objects.get(game_name = gameName)
            player_list = game.player_list_set.all()
            if player_list.filter(player_name=playerName).exists():
                join_error = 'Oops! Looks like you\'ve already joined. Select "rejoin" to rejoin an existing game. '
            else:
                playerId= player_list.count() + 1
                game.player_list_set.create(player_id = playerId, player_name = playerName, submit_state=0)
                request.session['gameName'] = gameName
                request.session['playerName'] = playerName
                incrementGameState(gameName,request)
        else:
            join_error = 'Something doesn\'t seem right. Double check the room code.'

        if join_error != '':
            print(join_error)
            return render(request, "join.html",{"join_error":join_error})
        return redirect('play')

def play(request):
    gameName = request.session['gameName']
    playerName = request.session['playerName']
    game = Game.objects.get(game_name=gameName)
    player= game.player_list_set.get(player_name=playerName)
    context = {
        "game" : game,
        "player" : player
    }
    request.session['gameState'] = getGameState(gameName)
    if request.method == 'GET':
        if game.game_state > game.player_list_set.count():
            return redirect('showmystack')
        # Always take from player to your "left"
        pullFromPlayerID = player.player_id - 1 if player.player_id != 1 else game.player_list_set.count()
        print(pullFromPlayerID)
        lastTurn = game.game_state - 1
        if game.game_state%2 == 0:
            # Writing Phase
            clue = 'descriptionary/{}_{}_{}.png'.format(gameName,pullFromPlayerID,lastTurn)
        else:
            # Drawing phase
            if game.game_state > 1:
                clue = game.player_list_set.get(player_id=pullFromPlayerID).text_clues.split('|')[int(game.game_state/2)]
            else:
                clue = 'Anything you want to draw'
        context["clue"] = clue
        print("clue is: " + clue)
    else:
        if game.game_state%2 == 0:
            textEntry = request.POST.get('text_description')
            player.text_clues = player.text_clues +'|'+textEntry
            player.save()
        else:
            submittedimg = request.POST.get('img_from_player')[22:]
            imgdata = binascii.a2b_base64(submittedimg)
            with open(os.path.join(settings.BASE_DIR,'descriptionary/static/descriptionary/{}_{}_{}.png'.format(gameName,player.player_id,game.game_state)),'wb') as f:
                f.write(imgdata)
        player.submit_state = game.game_state
        player.save()
        incrementGameState(gameName,request)
        return redirect('play')
    return render(request, "play.html", context)

def showmystack(request):
    gameName = request.session['gameName']
    playerName = request.session['playerName']
    game = Game.objects.get(game_name=gameName)
    player= game.player_list_set.get(player_name=playerName)
    stack = getPlayerStack(game, player)
    context = {
        "game" : game,
        "player" : player,
        "stack" : stack
    }
    return render(request, "showmystack.html", context)

# =============================== #
# ====== Helper Functions ======= #
# =============================== #
def incrementGameState(gameName,request):
    if gameName not in refreshState:
        initializeRefreshState(gameName)
    refreshState[gameName] = refreshState[gameName] + 1
    request.session['gameState'] = getGameState(gameName)

def initializeRefreshState(gameName):
    refreshState[gameName] = 1

def getGameState(gameName):
    if gameName not in refreshState:
        initializeRefreshState(gameName)
    return refreshState[gameName]

def getPlayerStack(game, player):
    out = []
    player_id = player.player_id
    num_players = game.player_list_set.count()
    for i in range(1,num_players + 1):
        entry = []
        target_player = player_id + i - 1
        if target_player > game.player_list_set.count():
            target_player = target_player - num_players
        entry.append(game.player_list_set.get(player_id=target_player).player_name)
        if i%2 == 0:
            # Writing Entry
            entry.append("text")
            entry.append(game.player_list_set.get(player_id=target_player).text_clues.split('|')[int(i/2)])
        else:
            # Drawing Entry
            entry.append("image")
            entry.append('descriptionary/{}_{}_{}.png'.format(game.game_name,target_player,i))
        out.append(entry)
    return out

def checkRefresh(request):
    gameName = request.session['gameName']
    cur_state = request.session['gameState']
    if cur_state != refreshState[gameName]:
        return HttpResponse('REFRESH')
    else:
        return HttpResponse('')
