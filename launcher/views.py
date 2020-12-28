from django.shortcuts import render
from django.http import HttpResponse
from descriptionary.models import Game
from django.conf import settings
import os, glob

def index(request):
    return HttpResponse('Launcher here.')

def performCleanup(request):
    
    # Descriptionary cleaning
    for gm in Game.objects.all():
        gameName = gm.game_name
        gm.delete()
        search = 'descriptionary/static/descriptionary/{}_*_*.png'.format(gameName)
        print('looking for ' + 'search')
        for pic in glob.iglob(os.path.join(settings.BASE_DIR,search)):
            if os.path.exists(pic):
                os.remove(pic)
                print(pic + ' removed!')


    return HttpResponse('<p>Done cleaning</p>')
