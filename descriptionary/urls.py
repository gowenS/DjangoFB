from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home'),
    path('host', views.host, name='host'),
    path('join', views.join, name='join'),
    path('play', views.play, name='play'),
    path('checkrefresh', views.checkRefresh, name='checkrefresh'),
    path('gameview', views.gameview, name='gameview'),
    path('host_start', views.host_start, name='host_start'),
    path('showmystack', views.showmystack, name='showmystack'),
    path('showplayerstacks', views.showplayerstacks, name='showplayerstacks'),
]